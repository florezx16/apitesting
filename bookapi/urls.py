from django.urls import path
from .views import *

bookapi_patterns = ([
    path('new-book/',view=BookListCreateView.as_view(),name='add'),
    path('get-book/<str:isbn>',view=BookRetrieveView.as_view(),name='get'),
    path('get-books/',view=BookListView.as_view(),name='get'),
    path('update-book/<str:isbn>',view=BookUpdateView.as_view(),name='update'),
    path('delete-book/<str:isbn>',view=BookDeleteView.as_view(),name='delete')
],'bookapi')