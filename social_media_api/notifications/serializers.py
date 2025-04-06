from rest_framework import serializers
from .models import Notification
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

class UserBriefSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'username')


class NotificationSerializer(serializers.ModelSerializer):
    
    recipient = UserBriefSerializer(read_only=True)
    actor = UserBriefSerializer(read_only=True)
    target_type = serializers.SerializerMethodField()
    target_id = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = ('id', 'recipient', 'actor', 'verb', 'description', 
                 'target_type', 'target_id', 'unread', 'timestamp')
        read_only_fields = ('id', 'recipient', 'actor', 'verb', 'description', 
                           'target_type', 'target_id', 'timestamp')
    
    def get_target_type(self, obj):
        if obj.target_content_type:
            return obj.target_content_type.model
        return None
    
    def get_target_id(self, obj):
        return obj.target_object_id