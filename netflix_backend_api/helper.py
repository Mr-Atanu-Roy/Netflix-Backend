from rest_framework_simplejwt.tokens import RefreshToken

from netflix_backend_api.models import NetflixUser, UserProfile

import datetime
from django.conf import settings
import pytz

# Get the timezone object for the timezone specified in settings.py
tz = pytz.timezone(settings.TIME_ZONE)

# Get the current time in the timezone
current_time = datetime.datetime.now(tz)
    
def get_user(email):
    '''This function reurns the user instance on passing email'''
    try:
        return NetflixUser.objects.get(email=email), None
    except NetflixUser.DoesNotExist:            
        return None, "Invalid Email"
    except Exception as e:
        return None, "Something went wrong"


def get_profile(user):
    '''get user profile instance'''
    try:
        return UserProfile.objects.get(user=user), None
    
    except UserProfile.DoesNotExist:
        return None, "User does not exists"
    except Exception as e:
        #return this if any other error occurs
        return None, "something went wrong"


def get_token(user):
    '''
    it will generate a new token for the given user object
    '''
    refresh = RefreshToken.for_user(user)
    
    return str(refresh), str(refresh.access_token) 






