from rest_framework import serializers

from netflix_backend_api.helper import current_time, get_user
import datetime

from netflix_backend_api.models import (
    NetflixUser,
    UserProfile,
    OTP,
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


class EmailVerifySerializer(serializers.Serializer):
    '''
    It will handel email verification
    '''
    
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=255)
        
        
    def validate(self, data):
        '''validate otp'''
        
        user, error = get_user(data.get("email"))
        
        if user is not None:
            ten_min_ago = current_time - datetime.timedelta(minutes=10)
            checkOTP = OTP.objects.filter(otp=data.get("otp"), user=user, is_expired=False, purpose="email_verification", created_at__gte=ten_min_ago).first()
            
            if user.is_verified:
                raise serializers.ValidationError("This email is already verified")
            
            if not checkOTP:
                raise serializers.ValidationError("OTP is expired")
            else:
                checkOTP.is_expired=True
                checkOTP.save()
                
        else:
            raise serializers.ValidationError(error)
            
        
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
        
        user, error = get_user(data.get("email"))
        
        if user is not None:
            ten_min_ago = current_time - datetime.timedelta(minutes=10)
            checkOTP = OTP.objects.filter(otp=data.get("otp"), user=user, is_expired=False, purpose="reset_password", created_at__gte=ten_min_ago).first()
            
            
            if not checkOTP:
                raise serializers.ValidationError("OTP is expired")
            else:
                checkOTP.is_expired=True
                checkOTP.save()
                
        else:
            raise serializers.ValidationError(error)
            
        
        return data
    
    
    def update(self, instance, validated_data):
        '''Update the password'''
        password = validated_data.get("password", None)
        if password is not None or password != "":
            instance.set_password(password)
            instance.save()
        
        return instance
        
    
    def create(self, validated_data):
        return validated_data
    
    
    
    
    