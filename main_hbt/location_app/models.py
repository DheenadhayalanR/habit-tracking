from django.db import models
from django.apps import apps
from django.utils import timezone
from django.conf import settings


# def get_default_user():
#     User = apps.get_model(settings.AUTH_USER_MODEL)  # get the actual model class
#     user = User.objects.first()  # get first user
#     return user.id if user else None # assign first user
# Create your models here.

class Location(models.Model):
    country_region_city_name = models.CharField(max_length=100) 
    latitude = models.FloatField()
    longitude = models.FloatField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # <-- Use this instead of 'auth.User'
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.country_region_city_name
    