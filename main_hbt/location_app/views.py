from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

from .models import Location
from .serializers import LocationSerializer

# 1. Your existing model view
class LocationView(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

# 2. Helper function to get geolocation (this part of your code was good!)
def get_ip_geolocation(ip_address):
    url = f"http://ipinfo.io/{ip_address}/json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# 3. Helper function to get the client's IP from a Django request
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    print("x_forwarded_for",x_forwarded_for)
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print("ip",ip)
    return ip

# 4. A new API View to handle the logic
class TrackLocationView(APIView):
    def get(self, request, *args, **kwargs):
        # Allow the user to pass an IP in the URL query, e.g., /track/?ip=8.8.8.8
        ip_address_to_track = request.GET.get('ip')
        
        # If no IP is provided in the URL, track their own IP automatically
        if not ip_address_to_track:
            ip_address_to_track = get_client_ip(request)
            
        geolocation_data = get_ip_geolocation(ip_address_to_track)
        
        if geolocation_data and "error" not in geolocation_data:
            # We return a JSON response instead of using print()
            return Response({
                "tracked_ip": ip_address_to_track,
                "country": geolocation_data.get('country'),
                "region": geolocation_data.get('region'),
                "city": geolocation_data.get('city'),
                "location": geolocation_data.get('loc')  # Contains "lat,long"
            })
        else:
            return Response({"error": "Failed to fetch geolocation data."}, status=400)
