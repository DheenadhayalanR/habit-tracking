from django.urls import path,include
from . import views



urlpatterns = [
    
    path('userprofile/',views.profile_update.as_view(),name='User profile'),
    path('bio/',views.bioRetrieveUpdate.as_view(),name="Profile Bio")
    # path('setgoal/',views.set_goal.as_view(),name='Set Goal'),
]