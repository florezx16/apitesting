from django.urls import path
from .views import GetStatus, GetRepairBay, SendTeapot, PhaseChange_diagram

app_name = 'alt_Score'
urlpatterns = [
    path(route='status/',view=GetStatus.as_view(),name='status'),
    path(route='repair-bay/',view=GetRepairBay.as_view(),name='repair-bay'),
    path(route='teapot/',view=SendTeapot.as_view(),name='teapot'),
    path(route='phase-change-diagram/',view=PhaseChange_diagram.as_view(),name='hase-change-diagram')
]
