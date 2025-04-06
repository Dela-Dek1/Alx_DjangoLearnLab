from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class UserBriefSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'username')


class CommentSerializer(serializers.ModelSerializer):
    
    author = UserBriefSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'author_id', 'content', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
        
    def create(self, validated_data):
        
        author_id = validated_data.pop('author_id', None)
        
        # If no author_id was provided, use the request user
        if not author_id and 'request' in self.context:
            validated_data['author'] = self.context['request'].user
        
        return super().create(validated_data)
        
    def validate(self, data):
        
        author_id = data.get('author_id')
        request = self.context.get('request')
        
        if author_id and request and request.user.id != author_id:
            raise serializers.ValidationError(
                "You can only create comments as yourself."
            )
        
        return data


class PostSerializer(serializers.ModelSerializer):
    
    author = UserBriefSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True, required=False)
    comment_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author', 'author_id', 
                 'created_at', 'updated_at', 'comment_count')
        read_only_fields = ('id', 'created_at', 'updated_at')
        
    def create(self, validated_data):
        
        author_id = validated_data.pop('author_id', None)
        
        # If no author_id was provided, use the request user
        if not author_id and 'request' in self.context:
            validated_data['author'] = self.context['request'].user
            
        return super().create(validated_data)
        
    def validate(self, data):
     
        author_id = data.get('author_id')
        request = self.context.get('request')
        
        if author_id and request and request.user.id != author_id:
            raise serializers.ValidationError(
                "You can only create posts as yourself."
            )
            
        return data


class PostDetailSerializer(PostSerializer):
    
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ('comments',)
