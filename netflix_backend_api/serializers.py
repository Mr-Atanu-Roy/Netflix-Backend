from rest_framework import serializers

from netflix_backend_api.helper import current_time, get_user, get_movie
import datetime

from netflix_backend_api.models import (
    NetflixUser,
    UserProfile,
    OTP,
    Movie,
    Trailer,
    Cast,
    Genres,
    Watchlist,
    Review
)


#SERIALIZERS

class RegisterSerializer(serializers.ModelSerializer):
    '''this serializer will handle user registrations'''
    
    class Meta:
        model = NetflixUser
        fields = ['email', 'password', 'first_name', 'last_name']
        
        #setting password to write only and first_name, last_name mandetory
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def create(self, validated_data):
        '''
        Overriding create method since password is not hassed by default 
        '''
        user = NetflixUser.objects.create(
            email=validated_data.get("email"), 
            first_name = validated_data.get("first_name"),
            last_name = validated_data.get("last_name")
        )
        user.set_password(validated_data.get("password"))  
        user.save()
        return user
  
    
   
class LoginSerializer(serializers.ModelSerializer):
    '''
    this serializer will handle user login
    '''
    
    email = serializers.EmailField()
    
    class Meta:
        model = NetflixUser
        fields = ["email", "password"]


    
class UserProfileSerializer(serializers.ModelSerializer):
    '''
    this serializer will handle user profile
    '''
    
    class Meta:
        model = UserProfile
        fields = ['country', 'date_of_birth', 'language', 'profile_picture']
        extra_kwargs = {
            'user': {'read_only': True},
        }



class OTPSerializer(serializers.Serializer):
    '''Handels get OTP request'''
    
    email = serializers.EmailField()
    purpose = serializers.CharField()
    
    def validate(self, data):
        _, error = get_user(data.get("email"))
        
        if error is not None:
            raise serializers.ValidationError(error)
        
        return data
    
    def create(self, validated_data):
        user, _ = get_user(validated_data.get("email"))
        newOTP = OTP.objects.create(user=user, purpose=validated_data.get("purpose"))
        return newOTP
    
    def update(self, instance, validated_data):
        pass
    


class EmailVerifySerializer(serializers.Serializer):
    '''
    It will handel email verification
    '''
    
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=255)
        
        
    def validate(self, data):
        '''validate otp'''

        if self.context.get("user"):
            user, _ = get_user(data.get("email"))
            
            if user.is_verified:
            
                raise serializers.ValidationError("This email is already verified")
            
            else:
                if data.get("otp"):
                    
                    ten_min_ago = current_time - datetime.timedelta(minutes=10)
                    checkOTP = OTP.objects.filter(otp=data.get("otp"), user=user, is_expired=False, purpose="email_verification", created_at__gte=ten_min_ago).first()
                    
                    
                    if not checkOTP:
                        raise serializers.ValidationError("Invalid OTP. OTP may be expired")
                    else:
                        checkOTP.is_expired=True
                        checkOTP.save()
                        
                else:
                    raise serializers.ValidationError("OTP is required")
            
        
        return data
    
    
    def update(self, instance, validated_data):
        '''set is_verified to true'''
        user, _ = get_user(validated_data.get("email"))
        user.is_verified = True
        user.save()
        
        return instance
    
    def create(self, validated_data):
        return validated_data

        
          
class ResetPasswordSerializers(serializers.Serializer):
    '''
    It will handel reset password
    '''
    
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=500)
        
        
    def validate(self, data):
        '''validate otp'''
        
        if data.get("password") is None:
            raise serializers.ValidationError("Password is required")
        
        if data.get("otp") is None:        
            raise serializers.ValidationError("OTP is required")
        
        user, _ = get_user(data.get("email"))
         
        ten_min_ago = current_time - datetime.timedelta(minutes=10)
        checkOTP = OTP.objects.filter(otp=data.get("otp"), user=user, is_expired=False, purpose="reset_password", created_at__gte=ten_min_ago).first()
        
        if not checkOTP:
            raise serializers.ValidationError("Invalid OTP. OTP may be expired")
        else:
            checkOTP.is_expired=True
            checkOTP.save()
            
        
        return data
    
    
    def update(self, instance, validated_data):
        '''Update the password'''
        password = validated_data.get("password", None)
        instance.set_password(password)
        instance.save()
        
        return instance
        
    
    def create(self, validated_data):
        return validated_data
    
    
class MovieSerializer(serializers.ModelSerializer):
    '''Handels movie model'''
    
    genres = serializers.SerializerMethodField()
    cast = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        exclude = ['created_at', 'updated_at']
        
    def get_genres(self, obj):
        return [genre.name for genre in obj.genres.all()]

    def get_cast(self, obj):
        return [cast.name for cast in obj.cast.all()]
        
        
class TrailerSerializer(serializers.ModelSerializer):
    '''Handels trailer model'''
    
    movie = serializers.CharField(source="movie.title")
    class Meta:
        model = Trailer
        exclude = ['created_at', 'updated_at']
        
        
class CastSerializer(serializers.ModelSerializer):
    '''Handels cast model'''
    
    class Meta:
        model = Cast
        exclude = ['created_at', 'updated_at']
    
    
class GenresSerializer(serializers.ModelSerializer):
    '''Handels Genres model'''
    
    class Meta:
        model = Genres
        exclude = ['created_at', 'updated_at']


class WatchlistSerializerGET(serializers.ModelSerializer):
    '''It will handel get request made to get user's watchlist'''
    
    movie = serializers.CharField(source="movie.title")
    class Meta:
        model = Watchlist
        fields = ['movie', 'created_at']
       
    
class WatchlistSerializerPOST(serializers.Serializer):
    '''Handels creation of user watchlist'''
       
    movie_slug = serializers.CharField()
    
    def validate(self, data):
        '''This validation is to check if movie is alredy added in watchlist'''
        
        if data.get("movie_slug"):
            #check if movie_slug is given
            try:
                movie = Movie.objects.get(movie_slug=data.get('movie_slug'))
            except Movie.DoesNotExist:
                raise serializers.ValidationError("Invalid movie")
            
            user, _ = get_user(self.context.get("user"))
            
            #check if movie is already added in watchlist
            watchlist = Watchlist.objects.filter(movie=movie, user=user)
            
            if len(watchlist) != 0:
                #if movie exists in watchlist raise validation error
                raise serializers.ValidationError("This movie is already in your watchlist")
            
        return data
            

    def create(self, validated_data):
        
        user, _ = get_user(self.context.get("user"))
        movie = Movie.objects.get(movie_slug=validated_data.get('movie_slug'))
        return Watchlist.objects.create(movie=movie, user=user)
    
    
class ReviewSerializer(serializers.ModelSerializer):
    '''Handels Watchlist model'''
    
    user = serializers.CharField(source='user.first_name', read_only=True)
    
    class Meta:
        model = Review
        fields = ['user', 'rating', 'comment', 'updated_at']
    
    
    def update(self, instance, validated_data):
            
        instance.rating = validated_data.get("rating", instance.rating)
        instance.comment = validated_data.get("comment", instance.comment)
        instance.save()
            
        return instance
    
    def create(self, validated_data):
        
        if self.context.get("user") and self.context.get("movie_slug"):
            user, _ = get_user(self.context.get("user"))
            movie, _ = get_movie(self.context.get("movie_slug"))
            
            check_review = Review.objects.filter(user=user, movie=movie)
            if len(check_review) > 0:
                raise serializers.ValidationError("You have already reviewd this movie")
            
        return Review.objects.create(user=user, movie=movie, rating=validated_data.get("rating"), comment=validated_data.get("comment"))



    
        
        