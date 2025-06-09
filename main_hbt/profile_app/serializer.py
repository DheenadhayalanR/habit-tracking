from rest_framework import serializers
from .models import UserProfile 


class Userprofileserializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = fields = [
            'codename', 'age', 'gender', 'height', 'weight',
            'career', 'contact', 'bio', 'profile_pic', 'user_name'
        ]

        
# class Setgoalserializer(serializers.ModelSerializer):

#     class Meta:
#         model = SetGoal
#         fields ='__all__'
        
        
