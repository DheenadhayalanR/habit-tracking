from django.db import models
from django.dispatch import receiver
from django.core.validators import RegexValidator 
from django.db.models.signals import post_save 
from authn_user.models import User 

# profile model
class UserProfile(models.Model):
    enum_gender ={
        "Male":"Male",
        "Female":"Female",
        "Others" : "Others"
    }
    user     = models.OneToOneField(User,on_delete=models.CASCADE)  #one-to-one relationeship
    codename = models.CharField(max_length=20)
    age      = models.PositiveSmallIntegerField(blank=True) 
    gender   = models.CharField(max_length=20, choices=enum_gender, blank=True)
    height   = models.DecimalField(max_digits=5, decimal_places=2,null=True) 
    weight   = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    career   = models.CharField(max_length=50,null=True)
    contact  = models.CharField(
        max_length=20,  
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',  # Example regex for international phone numbers
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ],null=True
    )
    bio         = models.CharField(max_length=500,null=True)
    profile_pic = models.ImageField(upload_to='user_images',null=True)


@receiver(post_save, sender=User)  
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
       UserProfile.objects.create(user=instance,
                                  codename = "@"+instance.username
                                  )
    instance.userprofile.save()

# SetGoal
# class Quest(models.Model):
#     typeofhb=(
#         ('PH','Physical health'),
#         ('MH','Mental health')
#     )
    
#     UserProfile_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE ,null=False)
#     habit_type = models.CharField(max_length=20, choices=typeofhb, default='PH')
    # exercise_name = models.CharField(max_length=20, choices=list_of_exercise, blank=True)     # Exercise 
    # sports_name = models.CharField(max_length=20, choices=list_of_Sports, blank=True)         # Sports

# Physical health
# Exercise model
# class Exercise(models.Model):

#     list_of_exercise = (
#         ('Push-ups','Push-ups'),
#         ('Pull-ups','Pull-ups'),
#         ('Bench Press','Bench Press')
#       )

#     Category_id = models.ForeignKey(SetGoal, on_delete=models.CASCADE)
#     exercise_name = models.Multi(max_length=20, choices=list_of_exercise, blank=True)
    

# # Sports model
# class Sports(models.Model):
    
#     list_of_Sports = (
#         ('Running','Running'),
#         ('Swimming','Swimming')
#     )
    
    # Category_id = models.ForeignKey(SetGoal, on_delete=models.CASCADE)
    # sports_name = models.CharField(max_length=20, choices=list_of_Sports, blank=True)

class Exercise(models.Model):
    
    # exercise_id = models.AutoField(primary_key=True)
    exercise_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    # type = models.CharField(max_length=20)  # EX or STRECH
    target_zones_major = models.CharField(max_length=100)
    target_zones_minor = models.CharField(max_length=100, blank=True, null=True)
    min_reps = models.PositiveIntegerField()
    max_reps = models.PositiveIntegerField()
    time_based = models.BooleanField(default=False)
    pose_tag = models.CharField(max_length=100)
    equipment = models.CharField(max_length=100, default="None")
    media_url = models.CharField(max_length=255)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.exercise_name
