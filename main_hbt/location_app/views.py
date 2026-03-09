from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

from .models import Location
from authn_user.models import User
from .serializers import LocationSerializer
import logging

logger = logging.getLogger(__name__)

# 1. Your existing model view

def get_ip_geolocation(ip_address):
    url = f"http://ipinfo.io/{ip_address}/json"
    response = requests.get(url)
    if response.status_code == 200:
        print(response.json())
        return response.json()
    return None

# 3. Helper function to get the client's IP from a Django request
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class LocationView(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def list(self, request, *args, **kwargs):

        tracked_ip = get_client_ip(request)
        geolocation_data = get_ip_geolocation(tracked_ip)
        logger.info("geolocation_data",geolocation_data)
       
        if geolocation_data and "error" not in geolocation_data:
            logger.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print("geolocation_data",geolocation_data)
            loc = geolocation_data.get("loc")

            if loc:
                latitude, longitude = loc.split(",")

                city = geolocation_data.get("city")
                region = geolocation_data.get("region")
                country = geolocation_data.get("country")

                location_name = f"{country}, {region}, {city}"

                print("location_name",location_name)    

                Location.objects.get_or_create(
                    user=request.user,
                    defaults={
                        "latitude": latitude,
                        "longitude": longitude,
                        "country_region_city_name": location_name
                    }
                )

        return super().list(request, *args, **kwargs)


class UpdateLocationView(generics.UpdateAPIView):
    queryset = Location.objects.all()
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
