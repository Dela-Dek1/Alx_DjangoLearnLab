from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class UserBriefSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'username', 'profile_picture')


class CommentSerializer(serializers.ModelSerializer):
    
    user = UserBriefSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ('id', 'post', 'user', 'content', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')


class PostSerializer(serializers.ModelSerializer):
    
    user = UserBriefSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    like_count = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ('id', 'user', 'content', 'image', 'created_at', 'updated_at', 
                 'comments', 'like_count', 'is_liked')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')
    
    def get_is_liked(self, obj):
        
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False


class PostCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ('id', 'content', 'image')
        read_only_fields = ('id',)


class CommentCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ('id', 'post', 'content')
        read_only_fields = ('id',)
