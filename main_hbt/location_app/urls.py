from django.urls import path
from .views import LocationView, TrackLocationView

urlpatterns = [
    path('locations/', LocationView.as_view(), name='location-list'),
    path('track/', TrackLocationView.as_view(), name='track-location'),
]