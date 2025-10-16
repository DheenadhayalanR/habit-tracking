from rest_framework import serializers
from .models import UserProfile 


class Userprofileserializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'codename','age', 'gender', 'height', 'weight',
            'career', 'contact','name'
        ]

class profilebioserializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = 'bio'
        
class profilepicserializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = 'profile_pic'
        
        
# class Setgoalserializer(serializers.ModelSerializer):

#     class Meta:
#         model = SetGoal
#         fields ='__all__'
        
        
