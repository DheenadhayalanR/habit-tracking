from django.urls import path
from .views import LocationView,UpdateLocationView

urlpatterns = [
    path('', LocationView.as_view(), name='location'),
    path('<int:id>/', UpdateLocationView.as_view(), name='update-location'),
]