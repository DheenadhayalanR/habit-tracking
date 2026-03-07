from django.urls import path,include
from . import views


urlpatterns = [
    path('status/',views.StatusCreate.as_view(),name='Status'),
    path('status/<int:pk>/',views.StatusUpdate.as_view(),name='Status Update'),
    path('<int:day_id>/workoutplan/',views.WorkoutPlanList.as_view(),name='Workout plan for days'),
    path('workoutprogress/',views.UpdateWorkoutProgress.as_view(),name='workout progress')
]