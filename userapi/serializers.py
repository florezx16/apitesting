from .models import UserProfile
from django.contrib.auth.models import User
from django.core.validators import *
from django.core.exceptions import ValidationError

from rest_framework import serializers

import re #Check regex expression

def checkPasswordNumber(value):
    if not re.search(r'[0-9]',value):
        raise serializers.ValidationError('Password field should contain at least 1 number value.')
    return value
        
def checkPasswordUpper(value):
    if not re.search(r'[A-Z]',value):
        raise serializers.ValidationError('Password field should contain at least 1 uppercase value')
    return value

def checkPasswordSpecial(value):
    if not re.search(r'[!@#$%&*._-]',value):
        raise serializers.ValidationError('Password field should contain at least 1 special character. Allow characters are ! @ # $ %% & * . _ -')
    return value

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        min_length = 5,
        max_length = 20,
        validators = [
            RegexValidator(regex='^[a-zA-Z0-9._-]+$',message='This field contains invalid characters. Allowed characters are letters, numbers, period, underscore, and hyphen.')
        ]
    )
    
    password = serializers.CharField(
        min_length = 8,
        max_length = 25,
        validators = [
            RegexValidator(regex='^[a-zA-Z0-9._!@#$%&*-]+$',message='This field contains invalid characters. Allowed characters are ! @ # $ %% & * . _ - '),
            checkPasswordNumber,
            checkPasswordUpper,
            checkPasswordSpecial
        ]
    )
    
    first_name = serializers.CharField(
        min_length = 3,
        max_length = 30,
        validators = [
            RegexValidator(regex='^[a-zA-Z]+$',message='This field contains unvalid characters')
        ]
    )
    
    last_name = serializers.CharField(
        min_length = 3,
        max_length = 30,
        validators = [
            MinLengthValidator(3),
            MaxLengthValidator(25),
            RegexValidator(regex='^[a-zA-Z]+$',message='This field contains unvalid characters')
        ]
    )
    
    email = serializers.EmailField(
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(50),
            EmailValidator,
        ]
    )
    
    class Meta():
        model = User
        fields = ['username','password','first_name','last_name','email']
        
    def validate_username(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('This username is already taken, please check.')
        return value
    
    
class UserProfileSerializer(serializers.ModelSerializer):
    
    address = serializers.CharField(
        min_length = 5,
        max_length = 50,
        validators = [
            RegexValidator(regex='^[a-zA-Z0-9 ,.\n\r]+$',message='This field contains invalid characters.')
        ]
    )
    
    phone_number = serializers.CharField(
        min_length = 10,
        max_length = 20,
        validators = [
            RegexValidator(regex='^[0-9 -]+$',message='This field contains invalid characters.')
        ]
    )
    
    about_me = serializers.CharField(
        min_length = 10,
        max_length = 50,
        validators = [
            RegexValidator(regex='^[a-zA-Z0-9 ,.\n\r]+$',message='This field contains invalid characters.')
        ]
    )
    
    class Meta():
        model = UserProfile
        fields = ['address','phone_number','about_me']
    