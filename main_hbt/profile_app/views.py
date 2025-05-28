from .models import UserProfile ,SetGoal
from .serializer import Userprofileserializer,Setgoalserializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics,permissions

class profile_update(generics.RetrieveUpdateAPIView):
    
    serializer_class = Userprofileserializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)
    

class set_goal(generics.ListCreateAPIView):

    serializer_class = Setgoalserializer
    permission_classes = [permissions.IsAuthenticated]


    def create(self, request, *args, **kwargs):

        data = request.data.copy()
        data['UserProfile_id'] = request.user.userprofile.id

        # get the value from the request
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get_queryset(self):
        return SetGoal.objects.filter(UserProfile_id=self.request.user.userprofile)

    
    