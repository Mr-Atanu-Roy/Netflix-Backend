from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import Usermanager
import uuid

from django.db.models.signals import post_save
from django.dispatch import receiver

from .utils import *

import random

from autoslug import AutoSlugField

from django.utils import timezone
current_time = timezone.now


#CHOICES
language_choices = (
    ("english", "English"),    
    ("hindi", "Hindi"),  
    ("bengali", "Bengali"), 
)

media_type_choices = (
    ("movie", "Movie"),    
    ("Series", "Series"),  
)

rating_choices = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)

otp_purpose_choices = (
    ("email_verification", "Email Verification"),
    ("reset_password", "Reset Password")
)

# Create your models here.
#MODELS
class NetflixUser(AbstractUser):
    '''
    Creating a custom user model which will use email field to login instead of username
    '''
    username = None
    email = models.EmailField(unique=True, verbose_name="Email Address")
    is_verified = models.BooleanField(default=False, verbose_name="Is Verified")
    
    objects = Usermanager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = 'auth_user'
        verbose_name_plural = 'Netflix User'
    
    def __str__(self):
        return self.email


class BaseModel(models.Model):
    '''
    Creating a base model
    '''
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
 
 
class OTP(BaseModel):
    user = models.ForeignKey(NetflixUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=255, null=True, blank=True)
    is_expired = models.BooleanField(default=False)
    purpose = models.CharField(choices=otp_purpose_choices, max_length=255, default="email_verification")
    
    class Meta:
        verbose_name_plural = "Auth OTP"
    
    def __str__(self):
        return f"{str(self.otp)}"
       

class UserProfile(BaseModel):
    '''
    User Profile models which has 1-1foreign key with user model. It stores all other necessary informations about User
    '''
    
    user = models.OneToOneField(NetflixUser, on_delete=models.CASCADE, verbose_name="User")
    country = models.CharField(max_length=255, blank=True, null=True, verbose_name="Country", default="india")
    date_of_birth = models.DateField(null=True, blank=True)
    language = models.CharField(max_length=255, choices=language_choices, default="english", verbose_name="Prefered Language")
    profile_picture = models.FileField(upload_to='user/profile', max_length=600, verbose_name="Profile Picture", blank=True,null=True)
    
    class Meta:
        verbose_name_plural = "Netflix User Profile"
    
    def __str__(self):
        return str(self.user.email)


class Genres(BaseModel):
    '''
    It will contain information about movie and series genres
    '''
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    class Meta:
        verbose_name_plural = "Media Genre"
    
    def __str__(self):
        return self.name
    
  
    
class Cast(BaseModel):
    '''
    It will contain information about the cast or actors
    '''
    
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    biography = models.TextField()
    image = models.FileField(upload_to='cast/', max_length=600)
    
    class Meta:
        verbose_name_plural = "Media Casts"

    def __str__(self):
        return self.name


class Trailer(BaseModel):
    '''
    It will contain information about the trailer of a movie or series 
    '''
    trailer_name = models.CharField(max_length=255, null=True)
    trailer_url = models.URLField(max_length=600)
    thumbnail = models.FileField(upload_to='media/thumbnail', max_length=600)
    release_date = models.DateField(default=current_time)
    
    class Meta:
        verbose_name_plural = "Media Trailer"
    
    def __str__(self):
        return str(self.trailer_name)
      

class Season(BaseModel):
    '''
    Contains name, description, poster and episode of a season
    '''
    
    name = models.CharField(max_length=255)
    season_slug = AutoSlugField(populate_from=name, unique=True, null=True)
    description = models.TextField(null=True, blank=True)
    season_no = models.IntegerField(default=0)
    season_poster = models.FileField(upload_to = 'media/season-poster/', max_length=600)
    trailer = models.OneToOneField(Trailer, on_delete=models.CASCADE, null=True, blank=True)
    
    
    
    def __str__(self):
        return f"{self.name}-S{self.season_no}"
    

class Episode(BaseModel):
    '''
    Contains name, description, url of episodes of a season
    '''
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    episode_slug = AutoSlugField(populate_from=name, unique=True, null=True)
    description = models.TextField(null=True, blank=True)
    episode_no = models.IntegerField(default=0)
    episode_url = models.URLField(max_length=600)
    
    def __str__(self):
        return f"{self.name}-E{self.episode_no}-S{self.season.name}"   
  
    
class Media(BaseModel):
    '''
    It will contain data of all movies and series
    '''
    
    media_type = models.CharField(max_length=10, choices=media_type_choices, default="movie")
    title = models.CharField(max_length=255)
    media_slug = AutoSlugField(populate_from=title, unique=True)
    description = models.TextField(null=True, blank=True)
    release_date = models.DateField(default=current_time)
    poster = models.FileField(upload_to = 'media/poster/', max_length=600)
    media_video = models.URLField(max_length=600, blank=True, null=True)
    genres = models.ManyToManyField(Genres)
    cast = models.ManyToManyField(Cast)
    trailer = models.OneToOneField(Trailer, on_delete=models.CASCADE)
    is_season = models.BooleanField(default=False)
    season = models.ForeignKey(Season, blank=True, null=True, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Media-Movies/Seasons"
    
    def __str__(self):
        return self.title


class Watchlist(BaseModel):
    '''
    It will contain the movies and series that a user will add to his watchlist
    '''
    
    user = models.OneToOneField(NetflixUser, on_delete=models.CASCADE, verbose_name="User")
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "User Watchlist"

    def __str__(self):
        return str(self.media.title)


class Review(BaseModel):
    '''
    Contains reviews of User for movies and series
    '''
    
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    user = models.ForeignKey(NetflixUser, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=rating_choices)
    comment = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "User Review"
    
    
    def __str__(self):
        return f"{self.media.title} - {self.user.first_name} - {self.rating}"

    


#SIGNALS
@receiver(post_save, sender=NetflixUser)
def NetflixUser_created_handler(sender, instance, created, *args, **kwargs):
    '''
    This signal which will send a greetings email and create a UserProfile and OTP instance each time after a new user register, i.e., a NetflixUser is created
    '''
    if created:                
        subject = "Greetings From Netflix"
        message = f"Thank you for signing up with Netflix {instance.first_name}.... You have signed up using email - {instance.email}, at {instance.date_joined}"
        
        #starting the thread to send email
        SendEmail(subject, message, instance.email).start()
        
        #creating a UserProfile instance
        newProfile = UserProfile.objects.create(user=instance)
        newProfile.save()
        
        #creating a OTP instance
        newOTP = OTP.objects.create(user=instance)
        newOTP.save()
        

@receiver(post_save, sender=OTP)
def OTP_handler(sender, instance, created, *args, **kwargs):
    '''
    This signal send email based on purpose of OTP after an otp instance has been created
    '''
    if created :
        
        if instance.otp is None:
            instance.otp = random.randint(100000, 999999)   #setting a random otp if otp field is none
            instance.save()
        
        if instance.purpose.lower() == "email_verification":
            subject = "Verify Your Email"
            message = f"Your OTP for verifying email - {instance.user} is : {instance.otp}. This OTP is valid for the next 10 mintutes only"
            
        elif instance.purpose.lower() == "reset_password":
            subject = "Reset Your Password"
            message = f"Your OTP for reseting password for email - {instance.user} is : {instance.otp}. This OTP is valid for the next 10 mintutes only"

    
        #starting the thread to send email
        SendEmail(subject, message, instance.user.email).start()
    
    