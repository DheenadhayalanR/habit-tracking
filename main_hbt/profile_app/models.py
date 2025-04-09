from django.db import models
from django.dispatch import receiver 
from django.db.models.signals import post_save 
from athun_user.models import User 

# profile model
class UserProfile(models.Model):

    user   = models.OneToOneField(User,on_delete=models.CASCADE)  #one-to-one relationeship
    age    = models.PositiveSmallIntegerField(null=True,blank=True) 
    height = models.DecimalField(max_digits=5, decimal_places=2,null=True) 
    weight = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    profile_pic = models.ImageField(upload_to='user_images',null=True)


@receiver(post_save, sender=User)  
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
       UserProfile.objects.create(user=instance)
    instance.userprofile.save()

# SetGoal
class SetGoal(models.Model):
    typeofhb=(
        ('PH','Physical health'),
        ('MH','Mental health')
    )

    list_of_Sports = (
        ('Running','Running'),
        ('Swimming','Swimming')
    )

    list_of_exercise = (
        ('Push-ups','Push-ups'),
        ('Pull-ups','Pull-ups'),
        ('Bench Press','Bench Press')
      )
    
    UserProfile_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    habit_type = models.CharField(max_length=20, choices=typeofhb, default='PH')
    exercise_name = models.CharField(max_length=20, choices=list_of_exercise, blank=True)     # Exercise 
    sports_name = models.CharField(max_length=20, choices=list_of_Sports, blank=True)         # Sports

# Physical health
# # Exercise model
# class Exercise(models.Model):

#     Category_id = models.ForeignKey(SetGoal, on_delete=models.CASCADE)
#     exercise_name = models.CharField(max_length=20, choices=list_of_exercise, blank=True)
    

# # Sports model
# class Sports(models.Model):
    
#     Category_id = models.ForeignKey(SetGoal, on_delete=models.CASCADE)
#     sports_name = models.CharField(max_length=20, choices=list_of_Sports, blank=True)