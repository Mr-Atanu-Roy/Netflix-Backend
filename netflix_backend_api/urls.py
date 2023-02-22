from django.urls import path, include
from netflix_backend_api.views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('profile/', UserProfileView.as_view(), name="user-profile"),
    path('get-otp/', GetOTPView.as_view(), name="get-opt"),
    path('email-verify/', EmailVerifyView.as_view(), name="email-verify"),
    path('reset-password/', ResetPassword.as_view(), name="reset-password"),
]
