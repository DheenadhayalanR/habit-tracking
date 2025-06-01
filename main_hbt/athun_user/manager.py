from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password

class Usermanager(BaseUserManager):
    
    def create_user(self,username,email,password, **extra_fields):
        email=self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user    

