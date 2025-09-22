from . import models
from . import serializers
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import generics,permissions,status
from .utils import generate_workoutplan , check_workout_progress

class StatusCreate(generics.CreateAPIView):
    
    queryset = models.Status.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.StatusSerializer
    
    def perform_create(self, serializer):
        try:
            # Save the data with user attached
            data = serializer.save(user=self.request.user.userprofile) #----> Why use user.userprofile
            
            # Call your workout plan generation logic
            if data:
                generate_workoutplan(data.exe_category, self.request.user.userprofile, data.id)
    
        except Exception as e:
            raise APIException(f"Failed to create workout plan: {str(e)}")
        
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
        
        # day_id = check_workout_progress(self.request.user.userprofile)
        try :
            # user_profile_id = self.request.user.userprofile
            day_id = self.kwargs.get('day_id')
            workout_progress = models.WorkoutProgress.objects
            
            if workout_progress.filter(day=day_id).exists():
                return models.WorkoutPlan.objects.filter(day=day_id)
            else:
                return "Not Found Day id"
        except :
            return "User entry not in Workout Progress"
        
    
class UpdateWorkoutProgress(generics.RetrieveUpdateAPIView):
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.WorkoutProgressSerializer
    
    # def get_queryset(self):
    #     return 
    

        
    
    
        
        
        
        
        