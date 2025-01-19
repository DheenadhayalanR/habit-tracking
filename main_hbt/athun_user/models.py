from django.db import models
from django.dispatch import receiver 
from athun_user.manager import Usermanager
from django.db.models.signals import post_save 
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin

# user model 
class User(AbstractBaseUser,PermissionsMixin):

    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone =  models.CharField(
        max_length=20,  # Adjust based on your needs
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',  # Example regex for international phone numbers
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ],null=True
    )
    password = models.CharField(max_length=250)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects=Usermanager()


# profile model
class Profile(models.Model):

    user   = models.OneToOneField(User,on_delete=models.CASCADE)  #one-to-one relationeship
    age    = models.PositiveSmallIntegerField(null=True,blank=True) 
    height = models.DecimalField(max_digits=5, decimal_places=2,null=True) 
    weight = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    profile_pic = models.ImageField(upload_to='user_images',null=True)


@receiver(post_save, sender=User)  
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
       Profile.objects.create(user=instance)
    instance.profile.save()



    
