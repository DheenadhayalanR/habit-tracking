from django.shortcuts import render
from rest_framework import generics,permissions
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from .utils import get_client_ip,get_ip_geolocation
from .models import Location
from authn_user.models import User
from .serializers import LocationSerializer
import logging

logger = logging.getLogger(__name__)

# 1. Your existing model view


class LocationView(generics.ListAPIView):
    queryset = Location.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LocationSerializer


class UpdateLocationView(generics.UpdateAPIView):
    queryset = Location.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LocationSerializer

    def perform_update(self, serializer):

        latitude,country_region_city_name,longitude=None,None,None

        tracked_ip = get_client_ip(self.request)
        geolocation_data = get_ip_geolocation(tracked_ip)

        if geolocation_data and "error" not in geolocation_data:
            latitude = geolocation_data.get('loc').split(',')[0]
            longitude = geolocation_data.get('loc').split(',')[1]
            name = geolocation_data.get('city')
            country = geolocation_data.get('country')
            region = geolocation_data.get('region')
            country_region_city_name = f"{country}, {region}, {name}"

        serializer.save(user=self.request.user,latitude=latitude, longitude=longitude,country_region_city_name=country_region_city_name)  

# 2. Helper function to get geolocation (this part of your code was good!)



# # 4. A new API View to handle the logic
# class TrackLocationView(APIView):
#     def get(self, request, *args, **kwargs):
#         # Allow the user to pass an IP in the URL query, e.g., /track/?ip=8.8.8.8
#         ip_address_to_track = request.GET.get('ip')
        
#         # If no IP is provided in the URL, track their own IP automatically
#         if not ip_address_to_track:
#             ip_address_to_track = get_client_ip(request)
            
#         geolocation_data = get_ip_geolocation(ip_address_to_track)
        
#         if geolocation_data and "error" not in geolocation_data:
#             # We return a JSON response instead of using print()
#             return Response({
#                 "tracked_ip": ip_address_to_track,
#                 "country": geolocation_data.get('country'),
#                 "region": geolocation_data.get('region'),
#                 "city": geolocation_data.get('city'),
#                 "location": geolocation_data.get('loc')  # Contains "lat,long"
#             })
#         else:
#             return Response({"error": "Failed to fetch geolocation data."}, status=400)
