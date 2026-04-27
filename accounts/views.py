import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from .models import OTP, Profile

User = get_user_model()


# OTP GENERATOR 
def generate_otp(user, purpose="verify"):
    
    OTP.objects.filter(user=user, purpose=purpose).delete()

   
    code = str(random.randint(100000, 999999))

    otp = OTP.objects.create(
        user=user,
        code=code,
        purpose=purpose
    )

    print("NEW OTP:", code)  

    return otp




#  RESEND OTP 
def resend_otp(request, user_id):
    user = User.objects.get(id=user_id)

    last_otp = OTP.objects.filter(user=user).order_by('-created_at').first()

    if last_otp and (timezone.now() - last_otp.created_at).seconds < 60:
        messages.error(request, "Wait 60 seconds before resending OTP")
        return redirect(request.META.get('HTTP_REFERER'))

    OTP.objects.filter(user=user, is_used=False).update(is_used=True)

    generate_otp(user, "verify")

    messages.success(request, "OTP resent successfully")
    return redirect(f"/accounts/verify/{user.id}/")


#  REGISTER 
import random

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.is_active = False
        user.is_email_verified = False
        user.save()

        generate_otp(user, "verify")

        print("REGISTER OTP GENERATED (DB)")

        print("REGISTER HIT - OTP CALLING")

        return redirect(f"/accounts/verify/{user.id}/")

    return render(request, "accounts/register.html")


# VERIFY OTP FOR REGISTRATION
def verify_otp(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        code = request.POST.get("otp", "").strip()

        print("ENTERED OTP:", code)

        otp = OTP.objects.filter(
            user=user,
            code=code,
            purpose="verify",
            is_used=False
        ).order_by("-created_at").first()

        print("DB OTPs:", list(OTP.objects.filter(user=user).values("code", "is_used")))

        if otp and otp.is_valid():
            user.is_active = True
            user.is_email_verified = True
            user.save()

            otp.is_used = True
            otp.save()

            login(request, user)

            OTP.objects.filter(user=user, purpose="verify").delete()

            return redirect("/accounts/profile/")

        messages.error(request, "Invalid OTP")

    return render(request, "accounts/verify.html")

# LOGIN 
from django.core.cache import cache

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid credentials")
            return redirect("login")

        if not user.check_password(password):
            messages.error(request, "Invalid credentials")
            return redirect("login")

        login(request, user)
        return redirect("/accounts/profile/")

    return render(request, "accounts/login.html")
# FORGOT PASSWORD
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "User not found")
            return redirect("forgot_password")

        generate_otp(user, "reset")

        return redirect(f"/accounts/reset-otp/{user.id}/")

    return render(request, "accounts/forgot_password.html")


# RESET OTP 
def reset_otp(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        code = request.POST.get("otp", "").strip()

        otp = OTP.objects.filter(
            user=user,
            code=code,
            purpose="reset",
            is_used=False
        ).order_by("-created_at").first()

        if otp and otp.is_valid():
            otp.is_used = True
            otp.save()

            request.session["reset_user_id"] = user.id

            return redirect("set_new_password")

        messages.error(request, "Invalid OTP")

    return render(request, "accounts/reset_otp.html")

def set_new_password(request):
    user_id = request.session.get("reset_user_id")

    if not user_id:
        return redirect("login")

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("set_new_password")

        user.set_password(password)
        user.save()

        del request.session["reset_user_id"]

        messages.success(request, "Password reset successful")
        return redirect("login")

    return render(request, "accounts/set_new_password.html")

#  LOGOUT 
def logout_view(request):
    logout(request)
    return redirect("/accounts/login/")


# PROFILE 
@login_required
def profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    return render(request, "accounts/profile.html", {"profile": profile})