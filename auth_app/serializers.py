from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','is_superuser', 'email']  # Add other fields as needed

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested UserSerializer to include username and other user fields

    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'profile_image', 'birth_date']  # Add fields as needed
