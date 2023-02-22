from django.shortcuts import render

from django.contrib import auth

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from netflix_backend_api.helper import get_token, get_user, get_profile

from netflix_backend_api.models import (
    OTP
)

from netflix_backend_api.serializers import (
    RegisterSerializer, 
    LoginSerializer,
    UserProfileSerializer,
    EmailVerifySerializer,
    ResetPasswordSerializers,
)


# Create your views here.


class RegisterView(APIView):
    '''
    This api is used to register new users
    '''

    def post(self, request, format=None):
        '''Handels post request'''
        
        register_serializer = RegisterSerializer(data=request.data)
        
        #check if data is valid
        if register_serializer.is_valid():
            #save user instance
            newUser = register_serializer.save() 
            
            #generating refresh token for new user
            refresh_token, access_token = get_token(newUser)
            
            #retirning this if data is valid
            response = {
                "status" : status.HTTP_201_CREATED,
                "data" : register_serializer.data,
                "refresh" : refresh_token,
                "access" : access_token,
                "message" : "user registered successfully"
            }
            
            return Response(response, status=status.HTTP_201_CREATED)
        
        #returning this if given data is invalid
        response = {
                "status" : status.HTTP_400_BAD_REQUEST,
                "data" : register_serializer.data,
                "refresh" : "",
                "access" : "",
                "message" : register_serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
        


class LoginView(APIView):
    '''
    This api will handel user login
    '''
    
    def post(self, request, format=None):
        '''Handels post request'''
        
        login_serializer = LoginSerializer(data=request.data)
        
        if login_serializer.is_valid():
            # get email and password if data is valid 
            email = login_serializer.validated_data.get("email")
            password = login_serializer.validated_data.get("password")
            
            #authenticate the user            
            user = auth.authenticate(request, email=email, password=password)
            
            if user is not None:              
                #get tokens for user is user exists
                refresh_token, access_token = get_token(user)
                
                response = {
                    "status": status.HTTP_200_OK,
                    "data" : request.data,
                    "refresh" : refresh_token,
                    "access" : access_token,
                    "message" : "login successfull"
                }
                
                return Response(response, status=status.HTTP_200_OK)
            
            else:
                #return this if data is not valid
                response = {
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "data" : request.data,
                    "refresh" : "",
                    "access" : "",
                    "error" : "Invalid Credentials"
                }
                
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
                
            
        #return this if email and password is not given
        response = {
            "status": status.HTTP_400_BAD_REQUEST,
            "data" : login_serializer.data,
            "refresh" : "",
            "access" : "",
            "message" : login_serializer.errors
        }
        
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                

class UserProfileView(APIView):
    '''
    This api will retrive, update user profile
    '''
    
    #setting authentication and permission classes
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    def get(self, request, format=None):
        '''Handel get request-Retrive profile'''
        
        #get the profile instance
        profile, error = get_profile(request.user)
        
        if profile is not None:
            #check if profile exists
            
            profile_serializer = UserProfileSerializer(profile)
            
            #return this
            response = {
                "status": status.HTTP_200_OK,
                "data": profile_serializer.data,
                "message": "Profile retrived"
            }
            return Response(response, status=status.HTTP_200_OK)
        
        else:
            #else return this
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "data": "",
                "message": error
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, format=None):
        '''Handel put request-Update profile'''
        
        #get user profile instance
        profile, error = get_profile(request.user)
        
        #check if profile exists
        if profile is not None:
        
            profile_serializer = UserProfileSerializer(profile, data=request.data, partial=True)
            
            if profile_serializer.is_valid():
                #if data is valid update it
                profile_serializer.save()
                
                #and return this
                response = {
                    "status": status.HTTP_201_CREATED,
                    "data": profile_serializer.data,
                    "message": "profile updated"
                }
                
                return Response(response, status=status.HTTP_201_CREATED)
            
            else:
                #if data is not valid return this
                response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "data": profile_serializer.data,
                    "error": profile_serializer.errors
                }
                
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            #else return this
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "data": "",
                "message": error
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
      
      

class GetOTPView(APIView):
    '''
    This API will generate otp
    '''
      
    def get(self, request):
        '''handel post request-Generate OTP'''
        
        #check if request.data has email and purpose
        if "email" in request.data and "purpose" in request.data:
            email = request.data.get('email')
            purpose = request.data.get('purpose')

            #get the user instance and errors
            user, error = get_user(email)
            
            if user is not None:
                #if user exists create otp
                newOTP = OTP.objects.create(user=user, purpose=purpose)
                newOTP.save()

                response = {
                    "status": status.HTTP_201_CREATED,
                    "data": {
                        "email": email,
                        "otp": str(newOTP),
                        "purpose": purpose
                    },
                    "message": f"OTP generated for {purpose}"
                }
                
                return Response(response, status=status.HTTP_201_CREATED)
            
            else:
                #otherwise return the error
                response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "data": {
                        "email": email,
                        "otp": "",
                        "purpose": purpose
                    },
                    "message": error
                }
                
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            #if email or purpose is not present in request.data return this
            response = {
                "status" : status.HTTP_400_BAD_REQUEST,
                "data": "",
                "message": "email and purpose are required"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
      
class EmailVerifyView(APIView):
    '''
    This api will verify email
    '''    
      
    def put(self, request):
        '''handel put request-verify otp'''
        
        #check if request.data has email, otp and purpose
        if "email" in request.data and "otp" in request.data:
            
            email = request.data.get('email')
                        
            #get the user instance
            user, error = get_user(email)
            
            #check if user exists
            if user is not None:
                serializer = EmailVerifySerializer(user, data=request.data, partial=True)
                if serializer.is_valid():
                    #if serializer is valid save it 
                    serializer.save()
                    response = {
                        "status": status.HTTP_200_OK,
                        "data": serializer.validated_data,
                        "message": "Password Updated"
                    }

                    return Response(response, status=status.HTTP_200_OK)
                
                else:
                    #else return this
                    response = {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "data": serializer.data,
                        "message": serializer.errors
                    }

                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
             
            else:
                #else return this
                response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "data": {
                        "email": email,
                        "otp": "",
                    },
                    "message": error
                }
                
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            #if email or otp or purpose is not present in request.data return this
            response = {
                "status" : status.HTTP_400_BAD_REQUEST,
                "data": "",
                "message": "email and otp are Required"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
            


class ResetPassword(APIView):
    '''
    This api will reset password
    '''
    
    def put(self, request):
        '''handel put request-update password'''
        
        if "email" in request.data and "otp" in request.data and "password" in request.data:
            
            #get the user instance
            user, error = get_user(request.data.get("email"))
            
            #check if user exists
            if user is not None:
                serializer = ResetPasswordSerializers(user, data=request.data, partial=True)
                
                if serializer.is_valid():
                    #if serializer is valid save it 
                    serializer.save()
                    response = {
                        "status": status.HTTP_200_OK,
                        "data": serializer.validated_data,
                        "message": "Password Updated"
                    }

                    return Response(response, status=status.HTTP_200_OK)
                
                else:
                    #else return this
                    response = {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "data": serializer.data,
                        "message": serializer.errors
                    }

                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
                
            else:
                #return this if user does not exists
                response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "data": "",
                    "message": error
                }

                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            #if email or otp or purpose is not present in request.data return this
            response = {
                "status" : status.HTTP_400_BAD_REQUEST,
                "data": "",
                "message": "email, password and otp are Required"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        



