from .models import User
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet 
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken 
from .serializer import RegisterSerializer,Loginserializer


# Create your views here.

class Registerviwe(ModelViewSet):
    
    http_method_names=['post']  
    serializer_class = RegisterSerializer
    permission_classes = (IsAuthenticated,)

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
    
    
class Loginview(ModelViewSet):

    http_method_names=['post']
    serializer_class = Loginserializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        
        email = request.data.get('email')
        password = request.data.get('password')

        # Use the authenticate function
        user = authenticate(request, email=email, password=password)

        if user is not None: 
            refresh = RefreshToken.for_user(user)  # Create a refresh token for the given user

            return Response({
                      'refresh': str(refresh), 
                      'access': str(refresh.access_token)  # Access token can be retrieved from the refresh token
                    })
        else:
             return Response("Invalid email or password")

