from rest_framework import generics, permissions, status, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Count
from .serializers import UserSerializer, AuthTokenSerializer, UserListSerializer

CustomUser = get_user_model()

class CreateUserView(generics.CreateAPIView):
   
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)

class CreateTokenView(ObtainAuthToken):
    
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })

class ManageUserView(generics.RetrieveUpdateAPIView):
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
       
        return self.request.user


class FollowUserView(generics.GenericAPIView):
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        
        users = CustomUser.objects.all()
        user_to_follow = get_object_or_404(users, id=user_id)
        user = request.user
        
        if user == user_to_follow:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        user.follow(user_to_follow)
        return Response({"status": "following"}, status=status.HTTP_200_OK)

class UnfollowUserView(generics.GenericAPIView):
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
       
        users = CustomUser.objects.all()
        user_to_unfollow = get_object_or_404(users, id=user_id)
        user = request.user
        
        if user == user_to_unfollow:
            return Response(
                {"detail": "You cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        user.unfollow(user_to_unfollow)
        return Response({"status": "unfollowed"}, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
   
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        return UserSerializer
    
    def get_serializer_context(self):
        
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    
    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        
        user_to_follow = self.get_object()
        user = request.user
        
        if user == user_to_follow:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        user.follow(user_to_follow)
        return Response({"status": "following"}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        
        user_to_unfollow = self.get_object()
        user = request.user
        
        if user == user_to_unfollow:
            return Response(
                {"detail": "You cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        user.unfollow(user_to_unfollow)
        return Response({"status": "unfollowed"}, status=status.HTTP_200_OK)