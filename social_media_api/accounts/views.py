from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import UserSerializer, UserRegisterSerializer
from .models import CustomUser  
from rest_framework import permissions


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()  # Use CustomUser here
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class FollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()  # Use CustomUser here
    
    def post(self, request, user_id):
        try:
            user_to_follow = CustomUser.objects.get(id=user_id)  # Use CustomUser here
            if user_to_follow == request.user:
                return Response({'error': 'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
            
            request.user.following.add(user_to_follow)
            return Response({'status': f'You are now following {user_to_follow.username}'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:  # Use CustomUser here
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()  # Use CustomUser here
    
    def post(self, request, user_id):
        try:
            user_to_unfollow = CustomUser.objects.get(id=user_id)  # Use CustomUser here
            
            if user_to_unfollow in request.user.following.all():
                request.user.following.remove(user_to_unfollow)
                return Response({'status': f'You have unfollowed {user_to_unfollow.username}'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'You were not following this user'}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:  # Use CustomUser here
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
