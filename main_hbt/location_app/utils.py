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

def create_location(request):
    try:
        tracked_ip = get_client_ip(request)
        geolocation_data = get_ip_geolocation(tracked_ip) 
        
        if geolocation_data and "error" not in geolocation_data:
            loc = geolocation_data.get("loc")

        if loc:
            latitude, longitude = loc.split(",")

            city = geolocation_data.get("city")
            region = geolocation_data.get("region")
            country = geolocation_data.get("country")

            location_name = f"{country}, {region}, {city}"

            Location.objects.create(
                user=request.user,
                latitude=latitude,
                longitude=longitude,
                country_region_city_name=location_name
            )
    except Exception as e:
        logger.error(f"Error creating location: {e}")