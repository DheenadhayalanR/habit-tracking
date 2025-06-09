from .models import UserProfile 
from .serializer import Userprofileserializer
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import generics,permissions,status

class profile_update(generics.RetrieveUpdateAPIView):
    
    serializer_class = Userprofileserializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        try:
            return UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            raise NotFound("User profile not found.")
    
    def perform_update(self, serializer):
        serializer.save()   
        

class bioRetrieveUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return UserProfile.objects.get(user=self.request.user)
        except:
            raise NotFound("Profile Bio not found.")

    def retrieve(self, request, *args, **kwargs):
        profile = self.get_object()
        return Response({"bio": profile.bio})
        
    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        new_bio = request.data.get('bio')

        try :
            if new_bio:
                profile.bio = new_bio
                profile.save()
                return Response({"bio": profile.bio}, status=status.HTTP_200_OK)
            else:
                return  Response({"error": "bio is required."}, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({"error": "Something issue in profile update ."}, status=status.HTTP_400_BAD_REQUEST)


# class set_goal(generics.ListCreateAPIView):

#     serializer_class = Setgoalserializer
#     permission_classes = [permissions.IsAuthenticated]


#     def create(self, request, *args, **kwargs):

#         data = request.data.copy()
#         data['UserProfile_id'] = request.user.userprofile.id

#         # get the value from the request
#         serializer = self.get_serializer(data=data)

#         if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#     def get_queryset(self):
#         return SetGoal.objects.filter(UserProfile_id=self.request.user.userprofile)

    
    