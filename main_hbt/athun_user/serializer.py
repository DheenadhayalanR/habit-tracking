from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
                                     max_length=250, min_length=8, 
                                     write_only=True, required=True,
                                    )
    email = serializers.EmailField(required=True, max_length=128)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    
    def create(self, validated_data):

        try:
            user = User.objects.get(email=validated_data['email'])
        except ObjectDoesNotExist:
            user = User.objects.create_user(**validated_data)
        return user
    

class Loginserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
    
    

class LogoutSerializer():
    pass