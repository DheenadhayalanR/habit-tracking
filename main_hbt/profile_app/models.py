from django.db import models
from django.dispatch import receiver
from django.core.validators import RegexValidator 
from django.db.models.signals import post_save 
from athun_user.models import User 

# profile model
class UserProfile(models.Model):
    enum_gender ={
        "Male":"Male",
        "Female":"Female",
        "Others" : "Others"
    }
    user    = models.OneToOneField(User,on_delete=models.CASCADE)  #one-to-one relationeship
    age     = models.PositiveSmallIntegerField(null=True,blank=True) 
    gender  = models.CharField(max_length=20, choices=enum_gender, blank=True)
    height  = models.DecimalField(max_digits=5, decimal_places=2,null=True) 
    weight  = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    career  = models.CharField(max_length=50,null=True)
    contact = models.CharField(
        max_length=20,  # Adjust based on your needs
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',  # Example regex for international phone numbers
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ],null=True
    )
    bio = models.CharField(max_length=500,null=True)
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
    
    UserProfile_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE ,null=False)
    habit_type = models.CharField(max_length=20, choices=typeofhb, default='PH')
    # exercise_name = models.CharField(max_length=20, choices=list_of_exercise, blank=True)     # Exercise 
    # sports_name = models.CharField(max_length=20, choices=list_of_Sports, blank=True)         # Sports

# Physical health
# Exercise model
class Exercise(models.Model):

    list_of_exercise = (
        ('Push-ups','Push-ups'),
        ('Pull-ups','Pull-ups'),
        ('Bench Press','Bench Press')
      )

    # Category_id = models.ForeignKey(SetGoal, on_delete=models.CASCADE)
    # exercise_name = models.Multi(max_length=20, choices=list_of_exercise, blank=True)
    

# # Sports model
class Sports(models.Model):
    
    list_of_Sports = (
        ('Running','Running'),
        ('Swimming','Swimming')
    )
    
    # Category_id = models.ForeignKey(SetGoal, on_delete=models.CASCADE)
    # sports_name = models.CharField(max_length=20, choices=list_of_Sports, blank=True)