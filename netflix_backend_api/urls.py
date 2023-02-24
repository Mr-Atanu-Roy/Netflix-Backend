from django.urls import path, include
from netflix_backend_api.views import *

urlpatterns = [
    #register and login related urls
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('profile/', UserProfileView.as_view(), name="user-profile"),
    path('get-otp/', GetOTPView.as_view(), name="get-opt"),
    path('email-verify/', EmailVerifyView.as_view(), name="email-verify"),
    path('reset-password/', ResetPassword.as_view(), name="reset-password"),
    
    #movie related urls
    path('movies/', ListMovieView.as_view(), name="movies"),
    path('movies/<movieSlug>', RetriveMovieView.as_view(), name="movies"),
    
    #trailer related urls
    path('trailer/', ListTrailerView.as_view(), name="trailer"),
]
