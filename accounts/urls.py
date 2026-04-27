from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("verify/<int:user_id>/", views.verify_otp, name="verify"),
    path("resend/<int:user_id>/", views.resend_otp, name="resend"),

    path("forgot/", views.forgot_password, name="forgot_password"),
    path("reset-otp/<int:user_id>/", views.reset_otp, name="reset_otp"),
    path("set-new-password/", views.set_new_password, name="set_new_password"),

    path("profile/", views.profile, name="profile"),
]