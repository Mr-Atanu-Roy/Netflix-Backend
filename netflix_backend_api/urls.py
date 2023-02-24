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
    path('movies/<slug:movie_slug>', RetriveMovieView.as_view(), name="movie-detail"),
    path('full-movie-detail/<slug:movie_slug>', FullMovieDetailView.as_view(), name="full-movie-detail"),
    
    #trailer related urls
    path('trailer/', ListTrailerView.as_view(), name="trailers"),
    path('trailer/<slug:movie_slug>', RetriveTrailerView.as_view(), name="trailer-detail"),
    
    #cast related urls
    path('cast/', ListCastView.as_view(), name="casts"),
    path('cast/<slug:movie_slug>', RetriveCastView.as_view(), name="cast-detail"),
    
    #cast related urls
    path('genres/', ListGenresView.as_view(), name="genres"),

    
]
