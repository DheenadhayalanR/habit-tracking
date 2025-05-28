from .models import User
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from .token_generate import get_tokens_for_user ,refresh_access_token
from .serializer import RegisterSerializer,Loginserializer


# Create your views here.

class Registerviwe(generics.CreateAPIView):

    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        email = request.data.get('email')

        if User.objects.filter(email=email).exists():

            return Response(
                {"error": "A user with this email already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate serializer data
        else:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Return validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Loginview(generics.CreateAPIView):

    serializer_class = Loginserializer

    def create(self, request):
        
        email = request.data.get('email')
        password = request.data.get('password')

        # Use the authenticate function
        user = authenticate(request, email=email, password=password)

        if user is not None: 
            refresh = get_tokens_for_user(user)  # Create a refresh token for the given user

            return Response({
                      'refresh': str(refresh['refresh']), 
                      'access' : str(refresh['access'])  # Access token can be retrieved from the refresh token
                    })
        else:
             return Response("Invalid email or password")


class RefershAccessToken(generics.CreateAPIView):

    def create(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")
        access_token = refresh_access_token(refresh_token)
        
        if access_token: 
            return Response({"access": access_token}, status=200)
        return Response({"error": "Invalid or expired refresh token"}, status=400)
