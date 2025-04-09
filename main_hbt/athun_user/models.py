from django.db import models
from athun_user.manager import Usermanager
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










    
