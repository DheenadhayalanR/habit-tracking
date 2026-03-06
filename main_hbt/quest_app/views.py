from . import models
from . import serializers
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import generics,permissions,status
from .utils import generate_workoutplan , check_workout_progress

class StatusCreate(generics.ListCreateAPIView):
    
    queryset = models.Status.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.StatusSerializer
    
    def perform_create(self, serializer):
        try:
            # Save the data with user attached
            data = serializer.save(user=self.request.user.userprofile)
            
            # Call your workout plan generation logic
            if data:
                generate_workoutplan(data.exe_category, self.request.user.userprofile, data.id)
    
        except Exception as e:
            raise APIException(f"Failed to create workout plan: {str(e)}")

class StatusUpdate(generics.RetrieveUpdateAPIView):

    queryset = models.Status.objects.all()
    serializer_class = serializers.StatusSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_update(self, serializer):
        try:
            # Save the updated status details
            user_profile = self.request.user.userprofile
            data = serializer.save(user=user_profile)
            
            # Deactivate the CURRENT active workout plans and progress to keep as history
            # models.WorkoutPlan.objects.filter(user_status=data, is_active=True).update(is_active=False)
            # models.WorkoutProgress.objects.filter(user_status=data, is_active=True).update(is_active=False)
            models.WorkoutPlan.objects.filter(user_status=data).delete()
            models.WorkoutProgress.objects.filter(user_status=data).delete()
            
            # Generate a fresh set of plans and progress for the newly updated status
            if data:
                generate_workoutplan(data.exe_category, user_profile, data.id)
        except Exception as e:
            raise APIException(f"Failed to update workout plan: {str(e)}")
        
class WorkoutPlanList(generics.ListAPIView):
   
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.WorkoutPlanSerializer
    
    def list(self, request, *args, **kwargs):
        
       try: 
           queryset = self.get_queryset()
           
           exercise_name = models.Exercise.objects.filter(
            workoutplan__in = queryset
           ).values_list('exercise_name', flat=True).distinct()
           
           level_values = models.Level.objects.filter(
                status__workoutplan__in = queryset
            ).values('reps','sets').distinct()
           
           data ={ "exercise_name": list(exercise_name),
                    "reps": list(level_values)[0]['reps'],
                    "sets": list(level_values)[0]['sets']
                           }
           return Response(data)
       
       except Exception as e:
           return Response({'error': str(e)}, status=400)
       
        # try:
        #     queryset =self.get_queryset()
        #     serializer = serializers.WorkoutPlanSerializer(queryset, many=True)
        #     print(serializer.data)
        #     return Response(serializer.data)      
        # except Exception as e:
        #    return Response({'error': str(e)}, status=400)  

    def get_queryset(self):
        
        try:
            day_id = self.kwargs.get('day_id')
            user_profile = self.request.user.userprofile
            workout_progress = models.WorkoutProgress.objects
            
            if workout_progress.filter(day=day_id, user_status__user=user_profile, is_active=True).exists():
                return models.WorkoutPlan.objects.filter(
                    day=day_id, 
                    user_status__user=user_profile,
                    is_active=True
                )
            else:
                return "Not Found Day id"
        except:
            return "User entry not in Workout Progress"
        
    
class UpdateWorkoutProgress(generics.RetrieveAPIView):
    
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.WorkoutProgressSerializer
    
    def get_object(self):
        try:
            user = self.request.user.userprofile
            # Only one status row exists for the user!
            status = models.Status.objects.get(user=user)
                       
            # Call your workout plan generation logic passing the status_id
            check_workout_progress(status_id=status.id)
            # Only grab the ACTIVE progress item (ignore history)
            return models.WorkoutProgress.objects.get(user_status=status, is_active=True)
    
        except Exception as e:
            raise APIException(f"Failed to Update workout Progress: {str(e)}")
        
    

        
    
    
        
        
        
        
        