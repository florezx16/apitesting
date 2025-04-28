from django.urls import path
from .views import *

userapi_patterns = ([
    path('newUser/',view=UserCreate_view.as_view(),name='add_user'),
],'userapi')