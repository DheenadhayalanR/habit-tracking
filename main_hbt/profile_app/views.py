from .models import UserProfile
from .serializer import Userprofileserializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics,permissions

class profile_update(generics.RetrieveUpdateAPIView):
    
    serializer_class = Userprofileserializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)