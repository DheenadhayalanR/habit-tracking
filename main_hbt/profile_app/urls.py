from django.urls import path,include
from . import views



urlpatterns = [
    
    path('userprofile/',views.profile_update.as_view(),name='User profile'),
]