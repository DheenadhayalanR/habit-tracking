from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from . import models


class DayPlanSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = models.DayPlan
        fields = ['day_name']
        
        
class ExerciseCategorySerializer(serializers.ModelSerializer):
  
    class Meta:
        model = models.ExerciseCategory
        fields = '__all__'
        
        
class ExerciseSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = models.Exercise
        fields = '__all__'
        
class StatusSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Status
        fields = ['level','exe_category','points']
        
    def validate(self, data):
        user = self.context['request'].user.userprofile
        if models.Status.objects.filter(user=user).exists():
            raise ValidationError("Status already exists for this user.")
        return data
        
class WorkoutPlanSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.WorkoutPlan
        fields = '__all__'

class WorkoutProgressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.WorkoutProgress
        fields = '__all__'