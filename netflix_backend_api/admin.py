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
    
    
class TrailerInline(admin.TabularInline):
    model = Trailer
    
class EpisodeInline(admin.StackedInline):
    model = Episode
    extra = 2
    
class SeasonInline(admin.StackedInline):
    model = Season
    
class MediaInline(admin.StackedInline):
    model = Media




class NetflixUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'is_verified', 'is_staff', 'last_login')
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


class OTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_expired', 'created_at')
    fieldsets = [
        ("OTP Details", {
            "fields": (
                ['user', 'is_expired', 'otp']
            ),
        }),
    ]
    
    search_fields = ["user", "is_expired"]
    
    
class MediaAdmin(admin.ModelAdmin):
    list_display = ('media_type', 'title', 'release_date', 'is_season', 'created_at')
    fieldsets = [
        ("Media Details", {
            "fields": (
                ['title', 'media_type', 'release_date', 'description']
            ),
        }),
        ("Trailer and Links", {
            "fields": (
                ['trailer', 'poster', 'media_video']
            ),
        }),
        ("Season", {
            "fields": (
                ['is_season', 'season']
            ),
        }),
        ("Cast and Genre", {
            "fields": (
                ['cast', 'genres']
            ), 'classes': ['collapse']
        }),
    ]
    
    
    search_fields = ["title", "media_type", "cast", "release_date"]


class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'season_no', 'created_at')
    fieldsets = [
        ("Season Details", {
            "fields": (
                ['name', 'description', 'season_no', 'season_poster']
            ),
        }),
    ]
    
    inlines = [EpisodeInline]
    
    search_fields = ["name"]
    
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'episode_no', 'season', 'created_at')
    fieldsets = [
        ("Season Details", {
            "fields": (
                ['name', 'episode_no','episode_url', 'season', 'description']
            ),
        }),
    ]
    
    search_fields = ["name", "season"]
    
    
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
    list_display = ('trailer_name', 'release_date', 'created_at')
    fieldsets = [
        ("Trailer Details", {
            "fields": (
                ['trailer_name', 'trailer_url', 'thumbnail', 'release_date']
            ),
        }),
    ]
    
    inlines = [MediaInline, SeasonInline]
    
    search_fields = ["trailer_name", 'country']


class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'media', 'created_at')
    fieldsets = [
        ("Watchlist Details", {
            "fields": (
                ['user', 'media']
            ),
        }),
    ]
    
    search_fields = ["user"]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'media', 'rating', 'created_at')
    fieldsets = [
        ("Rating Details", {
            "fields": (
                ['user', 'media', 'rating', 'comment']
            ),
        }),
    ]
    
    search_fields = ["user", "rating"]



#registering Netflixuser model
admin.site.register(NetflixUser, NetflixUserAdmin)

#registering OTP model
admin.site.register(OTP, OTPAdmin)

#registering Media model
admin.site.register(Media, MediaAdmin)

#registering Season model
admin.site.register(Season, SeasonAdmin)

#registering Episode model
admin.site.register(Episode, EpisodeAdmin)

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


