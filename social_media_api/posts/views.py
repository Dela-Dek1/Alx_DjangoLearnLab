from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer

# Create your views here.
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Add filtering options
        title = self.request.query_params.get('title')
        if title:
            queryset = queryset.filter(title__icontains=title)
        return queryset

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