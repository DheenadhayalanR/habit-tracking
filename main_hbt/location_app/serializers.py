import rest_framework.serializers
from .models import Location

class LocationSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'  