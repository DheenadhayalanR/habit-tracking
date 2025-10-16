from . import models
import random as ra
from django.db.models import F


def generate_workoutplan(Category, user, status_id):
    
    status_id = models.Status.objects.get(user=user)
    exercise_ids = models.Exercise.objects.filter(category = Category)
    exercise_ids.values_list('exercise_id', flat=True)
    exercise_list = list(exercise_ids)
    
    # list out the all day
    days = list(models.DayPlan.objects.order_by('day_name'))
    
    for _,day in enumerate(days):
        selected_exercises = ra.sample(exercise_list, k=2)
        
        for selected_exercise in selected_exercises:
            models.WorkoutPlan.objects.create(
                    user = user,                                        # -----------> why use user 
                    day = day,
                    status = models.Status.objects.get(id=status_id.id),
                    exercises = selected_exercise,
                    )
          
    models.WorkoutProgress.objects.create(
        day = models.DayPlan.objects.order_by('day_name').first(),
        total_day = 1,
        user_status = status_id
    )
        
    
def check_workout_progress(user):
    
    status_id = models.Status.objects.get(user=user)
    workout_progress = models.WorkoutProgress.objects.get(user_status=status_id)
    
    if workout_progress.workout_completed == True:
        result = models.WorkoutPlan.objects.update(
            day = workout_progress.day+1,
            total_day = F('total_day')+1,
            workout_completed = False
        )
        return result['day']
    else:
        return workout_progress.day