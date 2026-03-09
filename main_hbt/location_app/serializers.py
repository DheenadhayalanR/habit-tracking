import rest_framework.serializers
from .models import Location

class LocationSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'  
        read_only_fields = ('user',)

    def create(self, validated_data):
        return Location.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.country_region_city_name = validated_data.get('country_region_city_name', instance.country_region_city_name)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.user = validated_data.get('user', instance.user)
        instance.save()
        return instance