from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token

CustomUser = get_user_model()

class UserSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'bio', 'profile_picture', 'follower_count', 'following_count')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5},
            'id': {'read_only': True}
        }
    
    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        
        Token.objects.create(user=user)
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        
        if password:
            user.set_password(password)
            user.save()
            
        return user

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )
        
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')
        
        attrs['user'] = user
        return attrs