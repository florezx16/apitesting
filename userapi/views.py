from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import UserSerializer, UserProfileSerializer
from .utils import sanitizedParams
from .models import UserProfile

# Create your views here.
class UserCreate_view(generics.CreateAPIView):
    
    @swagger_auto_schema(
        operation_id='create',
        operation_summary="Add new user",
        operation_description="New user, need to use other API endpoints",
        tags=["User API"]
    )
        
    def get_serializer_class(self,serializerType='user'):
        if serializerType == 'profile':
            return UserProfileSerializer
        return UserSerializer
        
    def post(self, request, *args, **kwargs):
        #Get serializer each model
        serializer_user = self.get_serializer_class('user') #user serializer
        serializer_profile = self.get_serializer_class('profile') #profile serializer
        
        if request.data:
            #Separe user and profile information from request.data
            userData = sanitizedParams(request.data,serializer_user)
            profileData = sanitizedParams(request.data,serializer_profile)
            
            #Check sanitized patameters
            if userData and profileData:
                user = serializer_user(data=userData)
                if user.is_valid():#Validate user serializer
                    profile = serializer_profile(data=profileData)
                    if profile.is_valid():#Validate profile serializer
                        #Save the user information
                        new_user = user.save()
                        
                        #Save user profile information and add user key
                        new_profile = profile.validated_data
                        new_profile['user'] = new_user
                        UserProfile.objects.create(**new_profile) #Send unpackage data
                        
                        #Return response
                        return Response({
                            'result':True,
                            'detail':'User has been creted successfully'
                        },status=status.HTTP_201_CREATED)
                    else:
                        return Response({
                            'result':False,
                            'details':profile.errors
                        },status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        'result':False,
                        'details':user.errors
                    },status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'result':False,
                    'details':'Your provide data is not correct, please check and try again'
                },status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'result':False,
                'detail':'Data not provide, please check and try again.'
            },status=status.HTTP_400_BAD_REQUEST)
            
            

