from django.urls import path
from .views import ClientRetrieveView, ClientCheck

ofi_urlpatterns = [
    path('get_client/',view=ClientRetrieveView.as_view(),name='get_client'),
    path('run_check/',view=ClientCheck.as_view(),name='get_client'),
    
]
