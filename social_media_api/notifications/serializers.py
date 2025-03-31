# Create notifications/serializers.py
from rest_framework import serializers
from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'profile_picture']

class NotificationSerializer(serializers.ModelSerializer):
    actor = ActorSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'actor', 'verb', 'timestamp', 'is_read']
        read_only_fields = ['id', 'actor', 'verb', 'timestamp', 'is_read']