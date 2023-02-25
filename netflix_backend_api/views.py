from django.shortcuts import render
from django.contrib import auth


from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend


from netflix_backend_api.helper import get_token, get_user, get_profile, get_movie


from netflix_backend_api.serializers import (
    RegisterSerializer, 
    LoginSerializer,
    UserProfileSerializer,
    OTPSerializer,
    EmailVerifySerializer,
    ResetPasswordSerializers,
    MovieSerializer,
    TrailerSerializer,
    CastSerializer,
    GenresSerializer,
    WatchlistSerializerGET,
    WatchlistSerializerPOST,
    ReviewSerializer
)

from netflix_backend_api.models import (
    Movie,
    Trailer,
    Cast,
    Genres,
    Watchlist,
    Review
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
        
        otp_serializer = OTPSerializer(data=request.data)

        #check if data is valid
        if otp_serializer.is_valid():
            otp = otp_serializer.save()
            
            response = {
                    "status": status.HTTP_201_CREATED,
                    "data": {
                        "email": request.data.get("email"),
                        "otp": "OTP is send to your email",
                        "purpose": request.data.get("purpose")
                    },
                    "message": "OTP is send to you email"
                }
                
            return Response(response, status=status.HTTP_201_CREATED)
        
        else:
            #return this if validation fails
            response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "data": {
                        "email": request.data.get("email"),
                        "otp": None,
                        "purpose": request.data.get("purpose")
                    },
                    "message": otp_serializer.errors
                }
                
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
  
    
      
class EmailVerifyView(APIView):
    '''
    This api will verify email
    '''    
      
    def put(self, request):
        '''handel put request-verify otp'''
        
        email = request.data.get('email')
                    
        #get the user instance
        user, error = get_user(email)
        
        #check if user exists
        if user is not None:
            serializer = EmailVerifySerializer(user, data=request.data, partial=True, context={"user": user})
            if serializer.is_valid():
                #if serializer is valid save it 
                serializer.save()
                response = {
                    "status": status.HTTP_200_OK,
                    "data": serializer.validated_data,
                    "message": "Email Verified"
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
        


class ResetPassword(APIView):
    '''
    This api will reset password
    '''
    
    def put(self, request):
        '''handel put request-update password'''

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
    


class ListMovieView(ListAPIView):
    '''
    This api view will retrive all movies or filters movie based on query filter
    '''
    
    queryset = Movie.objects.all() 
    serializer_class = MovieSerializer
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'language', 'genres', 'cast']
    


class RetriveMovieView(RetrieveAPIView):
    '''
    This api view will retrive details of a movie as as per given movie slug
    '''
    queryset = Movie.objects.all() 
    serializer_class = MovieSerializer
    
    lookup_field = 'movie_slug' #setting movie_slug as lookup field instead of pk
            
              

class ListTrailerView(ListAPIView):
    '''
    This api view will retrive all trailer or filters trailer based on query filter
    '''
    
    queryset = Trailer.objects.all() 
    serializer_class = TrailerSerializer
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['movie']
        
        

class RetriveTrailerView(ListAPIView):
    '''
    This api view will retrive trailer details on basis of movie-slug
    '''
    
    def get(self, request, movie_slug):
        
        try:
            #check if movie exists
            movie = Movie.objects.get(movie_slug=movie_slug)
            trailer = Trailer.objects.get(movie=movie)
            
        except Movie.DoesNotExist or Trailer.DoesNotExist:
            #else return this
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "data": request.data,
                "message": "Movie does not exists"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "data": request.data,
                "message": "Some thing went wrong"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        
        trailer_serializer = TrailerSerializer(trailer)
        
        response = {
            "status": status.HTTP_200_OK,
            "data": trailer_serializer.data,
            "message": "Trailer Retrived"
        }
        return Response(response, status=status.HTTP_200_OK)
        

class ListCastView(ListAPIView):
    '''
    This api view will retrive all cast or filters cast based on query filter
    '''
    
    queryset = Cast.objects.all() 
    serializer_class = CastSerializer
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'country']


class RetriveCastView(APIView):
    '''
    This api view will retrive cast details on basis of movie slug
    ''' 
    
    def get(self, request, movie_slug):
        
        try:
            #check if movie exists
            movie = Movie.objects.get(movie_slug=movie_slug)
            cast = Cast.objects.filter(movie=movie)

        except Movie.DoesNotExist or Cast.DoesNotExist:
            #else return this
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "data": request.data,
                "message": "Movie does not exists"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "data": request.data,
                "message": "Some thing went wrong"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        if len(cast) > 1:
            # if more than one cast is there do this 
            cast_serializer = CastSerializer(cast, many=True)
        else:
            #else do this
            cast_serializer = CastSerializer(cast)
            
        response = {
            "status": status.HTTP_200_OK,
            "data": cast_serializer.data,
            "message": "Cast Retrived"
        }
        return Response(response, status=status.HTTP_200_OK)
     
 
class ListGenresView(ListAPIView):
    '''
    This api view will retrive all genres or filters genres based on query filter
    '''
    
    queryset = Genres.objects.all() 
    serializer_class = GenresSerializer
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']    
    

class FullMovieDetailView(APIView):
    '''
    This api view will retrive all details retaled to a movie (like movie, trailer, cast, genres details) on basis of slug
    '''
    
    def get(self, request, movie_slug):
        '''Handel get request- Retrive movie details'''
        try:
            #check if movie exists
            movie = Movie.objects.get(movie_slug=movie_slug)
            trailer = Trailer.objects.get(movie=movie)
            cast = Cast.objects.filter(movie=movie)
            genre = Genres.objects.filter(movie=movie)
            
            print(movie, trailer, cast, genre)

        except Movie.DoesNotExist or Trailer.DoesNotExist or Cast.DoesNotExist or Genres.DoesNotExist:
            #else return this
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "data": request.data,
                "message": "Movie does not exists"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "data": request.data,
                "message": "Some thing went wrong"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        
        movie_serializer = MovieSerializer(movie)
        trailer_serializer = TrailerSerializer(trailer)
        
        if len(cast) > 1:
            cast_serializer = CastSerializer(cast, many=True)
        else:
            cast_serializer = CastSerializer(cast)
        
        if len(genre) > 1:
            genre_serializer = GenresSerializer(genre, many=True)
        else:
            genre_serializer = GenresSerializer(genre)    
        
        response = {
            "status": status.HTTP_200_OK,
            "data": {
            
            "movie": movie_serializer.data,
            "trailer": trailer_serializer.data,
            "cast": cast_serializer.data,
            "genre": genre_serializer.data,
                
            },
            "message": "Movie details retrived"
        }
        
        return Response(response, status=status.HTTP_200_OK)


class WatchlistView(APIView):
    '''
    This API view will list and create user watchlist
    '''
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        '''handels post request'''
        
        #get the authenticated user
        user, _ = get_user(request.user)
        
        #get all the watchlist objs of authenticated user
        watchlist = Watchlist.objects.filter(user=user)

        if len(watchlist) == 0:
            #if nothing in watchlist return this
            response = {
                "status": status.HTTP_200_OK,
                "data": "",
                "message": "your watchlist is empty"
            }
            return Response(response, status=status.HTTP_200_OK)
        
        else:
            #else do this
            watchlist_serializer = WatchlistSerializerGET(watchlist, many=True)
            response = {
                "status": status.HTTP_200_OK,
                "data": watchlist_serializer.data,
                "message": f"your watchlist has {len(watchlist)} items"
            }
            return Response(response, status=status.HTTP_200_OK)    
        
    def post(self, request):
        '''Handel post request'''
             
        watchlist_serializer = WatchlistSerializerPOST(data=request.data, context={"user": request.user})
        
        if watchlist_serializer.is_valid():
            watchlist = watchlist_serializer.save()
            
            response = {
                "status": status.HTTP_200_OK,
                "data": watchlist_serializer.validated_data,
                "message": "movie added to your watchlist"
            }
            return Response(response, status=status.HTTP_200_OK)
        
        response = {
            "status": status.HTTP_400_BAD_REQUEST,
            "data": watchlist_serializer.data,
            "message": watchlist_serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
            

class WatchlistDeleteView(APIView):
    '''This view will delete user watchlist'''

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]    
        
    
    def delete(self, request, movie_slug):
        '''Handels delete request-Delete a watchlist'''
        
        user, _ = get_user(request.user)
        
        try:
            movie = Movie.objects.get(movie_slug=movie_slug)
        except Movie.DoesNotExist:
            response = {
                "status" : status.HTTP_400_BAD_REQUEST,
                "data": "",
                "message": "Movie not found"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        watchlist = Watchlist.objects.filter(user=user, movie=movie)
        if len(watchlist) > 0:
            watchlist.delete()
            
            response = {
                "status" : status.HTTP_404_NOT_FOUND,
                "data": "",
                "message": "Movie deleted"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        
        response = {
            "status" : status.HTTP_400_BAD_REQUEST,
            "data": "",
            "message": "This movie is not in your watchlist"
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)



class ReviewRetriveView(APIView):
    '''This API will retrive all reviews of a perticular movie based on movie_slug'''
    
    def get(self, request, movie_slug):
        
        try:
            movie = Movie.objects.get(movie_slug=movie_slug)
        except Movie.DoesNotExist:
            response = {
                "status" : status.HTTP_400_BAD_REQUEST,
                "data": "",
                "message": "Movie not found"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        reviews = Review.objects.filter(movie=movie)
        
        if len(reviews) == 0:
            response = {  
            "status" : status.HTTP_400_BAD_REQUEST,
                "data": "",
                "message": "No review till now for this movie"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            review_serializer = ReviewSerializer(reviews, many=True)
            
            response = {  
            "status" : status.HTTP_200_OK,
                "data": review_serializer.data,
                "message": "review retrived"
            }
            return Response(response, status=status.HTTP_200_OK)
    

class ReviewCreateView(APIView):
    '''This api will create or update user review'''
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self, request, movie_slug):
        '''handels post request - Create user review'''
        review_serializer = ReviewSerializer(data=request.data, context={"user": request.user, "movie_slug": movie_slug})
        
        if review_serializer.is_valid():
            review = review_serializer.save()
            
            response = {
                "status": status.HTTP_201_CREATED,
                "data": {
                    "movie": str(review.movie),    
                    "rating": review.rating,    
                    "comment": review.comment,    
                },
                "message": "Review posted"
            }
            
            return Response(response, status=status.HTTP_201_CREATED)
        
        response = {
            "status": status.HTTP_400_BAD_REQUEST,
            "data": review_serializer.data,
            "message": review_serializer.errors
        }
        
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, movie_slug):
        '''handels put request - update user review'''
        
        movie, _ = get_movie(movie_slug)
        
        if movie is None:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "data": "",
                "message": "Movie does not exists"
            }
            
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        review = Review.objects.get(user=request.user, movie=movie)
        review_serializer = ReviewSerializer(review, data=request.data, partial=True, context={"user": request.user, "movie_slug": movie_slug})
            
        if review_serializer.is_valid():
            #if data is valid update it
            review_serializer.save()
            
            #and return this
            response = {
                "status": status.HTTP_201_CREATED,
                "data": review_serializer.data,
                "message": "review updated"
            }
            
            return Response(response, status=status.HTTP_201_CREATED)
        
        else:
            #if data is not valid return this
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "data": review_serializer.data,
                "error": review_serializer.errors
            }
            
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        