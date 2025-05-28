from rest_framework import serializers
from .models import UserProfile ,SetGoal


class Userprofileserializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['age','height','weight','profile_pic']

class Setgoalserializer(serializers.ModelSerializer):

    class Meta:
        model = SetGoal
        fields ='__all__'
        
        
