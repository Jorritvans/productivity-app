from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Following

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']  # Add 'id' here
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Following
        fields = ['id', 'follower', 'followed']