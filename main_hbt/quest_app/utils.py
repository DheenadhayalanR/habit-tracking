from . import models
import random as ra
from django.db.models import F


def generate_workoutplan(Category, user, status_id):
    
    status_instance = models.Status.objects.get(id=status_id)
    exercise_ids = models.Exercise.objects.filter(category = Category)
    exercise_ids.values_list('exercise_id', flat=True)
    exercise_list = list(exercise_ids)
    # list out the all day
    days = list(models.DayPlan.objects.order_by('day_name'))
    
    for _,day in enumerate(days):
        selected_exercises = ra.sample(exercise_list, k=2)
        for selected_exercise in selected_exercises:
            models.WorkoutPlan.objects.create(
                    # user = user,                                        # -----------> why use user 
                    day = day,
                    user_status = status_instance,
                    exercises = selected_exercise,
                    )    
    models.WorkoutProgress.objects.create(
        day = models.DayPlan.objects.order_by('day_name').first(),
        total_day = 1,
        user_status = status_instance
    )
        
    
def check_workout_progress(status_id):
    
    # Grab the active progress so we don't accidentally update history items
    # workout_progress = models.WorkoutProgress.objects.get(user_status=status_id, is_active=True)
    workout_progress = models.WorkoutProgress.objects.get(user_status=status_id)
    
    workout_progress.workout_completed = True
    workout_progress.save(update_fields=['workout_completed'])
    
    if workout_progress.workout_completed:
        print(workout_progress.workout_completed,workout_progress.day)
        # day_plan = DayPlan.objects.get(pk=2)  
        # result = models.WorkoutProgress.objects.update(
        workout_progress.day =2 
        workout_progress.total_day += 1
        workout_progress.workout_completed = False
        workout_progress.save(update_fields=['day', 'total_day', 'workout_completed'])
        # )
        return workout_progress
    else:
        print("idddd",workout_progress.workout_completed)
        return workout_progress.day