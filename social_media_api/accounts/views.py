from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Q
from .models import Post, Comment
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
   
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']
    
    def get_queryset(self):
        
        queryset = Post.objects.all().annotate(comment_count=Count('comments'))
        return queryset
        
    def get_serializer_class(self):
        
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        
        serializer.save(author=self.request.user)
    
    @action(detail=False, methods=['get'])
    def feed(self, request):
        
        user = request.user
        followed_users = user.following.all()
        
        # Get posts from followed users
        queryset = Post.objects.filter(
            author__in=followed_users
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-created_at')
        
        # Apply pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class FeedView(APIView):
   
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        
        user = request.user
        followed_users = user.following.all()
        
        posts = Post.objects.filter(
            author__in=followed_users
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-created_at')
        
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    
    def perform_create(self, serializer):
        
        serializer.save(author=self.request.user)
    
    def get_queryset(self):
        
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post', None)
        
        if post_id is not None:
            queryset = queryset.filter(post__id=post_id)
            
        return queryset