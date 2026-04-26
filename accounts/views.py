from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == "POST":
        user = User.objects.create_user(
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password=request.POST.get('password')
        )

        login(request, user)
        return redirect('food_list')

    return render(request, 'accounts/register.html')

def user_login(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )

        if user:
            login(request, user)
            return redirect('food_list')

    return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.bio = request.POST.get('bio')
        profile.location = request.POST.get('location')
        profile.phone_number = request.POST.get('phone_number')
        profile.image = request.FILES.get('image')

        profile.save()
        return redirect('profile')

    return render(request, 'accounts/profile.html', {'profile': profile})