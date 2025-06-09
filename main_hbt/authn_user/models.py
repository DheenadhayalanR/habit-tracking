from django.db import models
from authn_user.manager import Usermanager
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin

# user model 
class User(AbstractBaseUser,PermissionsMixin):

    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=250)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects=Usermanager()










    
