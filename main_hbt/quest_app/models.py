from django.db import models
from profile_app.models import UserProfile



# Default Date Table List
# Day plan based on the level its default model  
class DayPlan(models.Model):
    
    day_name = models.CharField(max_length=5)

# Exercise Category plan based on the level its default model  
class ExerciseCategory(models.Model):
    
    category_name= models.CharField(max_length=50)
    category_description = models.TextField(blank=True, null=True)
    
    # def __str__(self):
    #     return self.category_name
    
# Exercise based on the level its default model
class Exercise(models.Model):
    
    exercise_id = models.AutoField(primary_key=True)
    exercise_name = models.CharField(max_length=100)
    category = models.ManyToManyField(ExerciseCategory)   # ---> try  One2many name also category_id and learn about Foreignkey
    description = models.TextField(blank=True, null=True)
    target_zones_major = models.CharField(max_length=100, null=True)
    target_zones_minor = models.CharField(max_length=100, blank=True, null=True)
    equipment = models.CharField(max_length=100, default="None")
    # min_reps = models.PositiveIntegerField()
    # max_reps = models.PositiveIntegerField()
    # time_based = models.BooleanField(default=False)
    # pose_tag = models.CharField(max_length=100)
    # media_url = models.CharField(max_length=255)
    # remarks = models.TextField(blank=True, null=True)

    # def __str__(self):
    #     return self.exercise_name
    
# User Level calculate
class Level(models.Model):
    level_list={
        "Beginner":"Beginner",
        "Intermediate" :"Intermediate",
        "Advanced" :"Advanced"
    }
    level = models.CharField(max_length=40)
    reps = models.IntegerField()
    sets = models.IntegerField()
    
    
# level Stat of the user 
class Status(models.Model):
    # only unique user in the status
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=False)
    level = models.ForeignKey(Level,on_delete=models.CASCADE)
    exe_category = models.ForeignKey(ExerciseCategory, on_delete=models.CASCADE)
    points = models.IntegerField(default=10)
    
    
# Workout plan based on the level its default model  
class WorkoutPlan(models.Model):
    
    status = models.ForeignKey(Status,on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    day = models.ForeignKey(DayPlan, on_delete=models.CASCADE)
    exercises = models.ForeignKey(Exercise,on_delete=models.CASCADE)
     
    # def __str__(self):
    #     return self.day

class WorkoutProgress(models.Model):
    
    user_status = models.ForeignKey(Status, on_delete = models.CASCADE)
    day = models.ForeignKey(DayPlan, on_delete = models.CASCADE)
    total_day = models.IntegerField(null=True)
    workout_completed = models.BooleanField(default=False)
    
    
