from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification
from django.views.generic import ListView
from django.http import JsonResponse
from rest_framework.generics import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
def home(request):
    return JsonResponse({"message": "Welcome to the Social Media API!"})


class FeedView(APIView):
    def get(self, request):
        return Response({'message': 'This is the feed.'})


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        # Using generics.get_object_or_404(Post, pk=pk) here to retrieve the post by primary key
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        
        # Using Like.objects.get_or_create(user=request.user, post=post) here to handle the like creation
        like, created = Like.objects.get_or_create(user=user, post=post)

        if created:
            # Only create notification if the post is liked for the first time
            if post.author != user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=user,
                    verb='liked your post',
                    content_type=ContentType.objects.get_for_model(post),
                    object_id=post.id
                )
            return Response({'status': 'post liked'}, status=status.HTTP_201_CREATED)
        
        return Response({'status': 'post already liked'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        # Using generics.get_object_or_404(Post, pk=pk) here to retrieve the post by primary key
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        
        try:
            # Try to get the like record for the user and the post
            like = Like.objects.get(user=user, post=post)
            like.delete()  # Delete the like if it exists
            return Response({'status': 'post unliked'}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({'error': 'you did not like this post'}, status=status.HTTP_400_BAD_REQUEST)
        
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    
    def get_queryset(self):
        if self.kwargs.get('post_pk'):
            return Comment.objects.filter(post_id=self.kwargs['post_pk'])
        return Comment.objects.none()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.kwargs.get('post_pk'):
            context['post_id'] = self.kwargs['post_pk']
        return context

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
    
        post_id = self.kwargs.get('post_pk')
        if post_id:
            post = Post.objects.get(id=post_id)
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb='commented on your post',
                    content_type=ContentType.objects.get_for_model(post),
                    object_id=post.id
            )
    
        return response
