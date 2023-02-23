from django.contrib import admin
from .models import *


# Register your models here.

class ProfileInline(admin.TabularInline):
    model = UserProfile
    
class WatchlistInline(admin.TabularInline):
    model = Watchlist
    
class ReviewInline(admin.TabularInline):
    model = Review
    extra = 2
    
    
class TrailerInline(admin.StackedInline):
    model = Trailer
    

class NetflixUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'is_verified', 'is_staff', 'last_login', 'date_joined')
    fieldsets = [
        ("User Details", {
            "fields": (
                ['email', 'password', 'first_name', 'last_name']
            ),
        }),
        ("More Details", {
            "fields": (
                ['is_verified', 'date_joined', 'last_login']
            ), 'classes': ['collapse']
        }),
        ("Permissions", {
            "fields": (
                ['is_staff', 'is_superuser', 'is_active', 'user_permissions', 'groups']
            ),
        }),
    ]
    
    inlines = [ProfileInline, WatchlistInline, ReviewInline]
    
    search_fields = ["email", "first_name", "last_name", "is_verified"]
    
    
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', 'language', 'created_at')
    fieldsets = [
        ("User Details", {
            "fields": (
                ['user', 'profile_picture', 'country', 'date_of_birth', 'language']
            ),
        }),
    ]

    
    search_fields = ["user", "country", "language"]


class OTPAdmin(admin.ModelAdmin):
    list_display = ('otp', 'user', 'purpose', 'is_expired', 'created_at')
    fieldsets = [
        ("OTP Details", {
            "fields": (
                ['user', 'purpose', 'is_expired', 'otp']
            ),
        }),
    ]
    
    search_fields = ["user", "is_expired"]
    
    
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'created_at')
    fieldsets = [
        ("Movie Details", {
            "fields": (
                ['title', 'release_date', 'description']
            ),
        }),
        ("Movie Genre", {
            "fields": (
                ['genres']
            )
        }),
        ("Poster and Link", {
            "fields": (
                ['movie_video_url', 'poster1', 'poster2']
            ),
        }),
    ]
    
    inlines = [TrailerInline]
    
    search_fields = ["title", "cast", "release_date"]

   
class GenresAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    fieldsets = [
        ("Genre Details", {
            "fields": (
                ['name', 'description']
            ),
        }),
    ]
    
    search_fields = ["name"]
    
    
class CastAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'created_at')
    fieldsets = [
        ("Cast Details", {
            "fields": (
                ['name', 'country', 'date_of_birth', 'image', 'biography']
            ),
        }),
    ]
    
    search_fields = ["name", 'country']


class TrailerAdmin(admin.ModelAdmin):
    list_display = ('movie', 'release_date', 'created_at')
    fieldsets = [
        ("Movie Details", {
            "fields": (
                ['movie']
            ),
        }),
        ("More Details", {
            "fields": (
                ['trailer_url', 'release_date']
            ),
        }),
    ]

    
    search_fields = ["movie"]


class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'created_at')
    fieldsets = [
        ("Watchlist Details", {
            "fields": (
                ['user', 'movie']
            ),
        }),
    ]
    
    search_fields = ["user"]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'rating', 'created_at')
    fieldsets = [
        ("Rating Details", {
            "fields": (
                ['user', 'movie', 'rating', 'comment']
            ),
        }),
    ]
    
    search_fields = ["user", "rating"]



#registering Netflixuser model
admin.site.register(NetflixUser, NetflixUserAdmin)

#registering Netflixuser model
admin.site.register(UserProfile, UserProfileAdmin)

#registering OTP model
admin.site.register(OTP, OTPAdmin)

#registering Movie model
admin.site.register(Movie, MovieAdmin)

#registering Genres model
admin.site.register(Genres, GenresAdmin)

#registering Cast model
admin.site.register(Cast, CastAdmin)

#registering Trailer model
admin.site.register(Trailer, TrailerAdmin)

#registering Watchlist model
admin.site.register(Watchlist, WatchlistAdmin)

#registering Review model
admin.site.register(Review, ReviewAdmin)



