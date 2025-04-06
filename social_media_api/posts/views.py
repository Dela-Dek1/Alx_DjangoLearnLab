from rest_framework import viewsets, permissions, filters, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Q
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer, LikeSerializer
from .permissions import IsAuthorOrReadOnly
from notifications.models import Notification


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
        following_users = user.following.all()
        
        queryset = Post.objects.filter(author__in=following_users).order_by('-created_at')
        
        # Apply pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        
        # Check if user already liked the post
        if post.likes.filter(id=user.id).exists():
            return Response(
                {"detail": "You have already liked this post."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Create like object
        like = Like.objects.create(user=user, post=post)
        
        # Create notification for post author if not the same user
        if post.author != user:
            content_type = ContentType.objects.get_for_model(post)
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb='liked',
                description=f"{user.username} liked your post.",
                target_content_type=content_type,
                target_object_id=post.id
            )
            
        return Response(
            {"detail": "Post liked successfully."},
            status=status.HTTP_201_CREATED
        )
        
    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        
        post = self.get_object()
        user = request.user
        
        # Check if user has liked the post
        if not post.likes.filter(id=user.id).exists():
            return Response(
                {"detail": "You have not liked this post."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Delete the like
        Like.objects.filter(user=user, post=post).delete()
            
        return Response(
            {"detail": "Post unliked successfully."},
            status=status.HTTP_200_OK
        )


class FeedView(APIView):
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        
        user = request.user
        following_users = user.following.all()
        
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


class LikeView(APIView):
   
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        Like.objects.get_or_create(user=request.user, post=post)
        
        # Create notification for post author if not the same user
        if post.author != request.user:
            content_type = ContentType.objects.get_for_model(post)
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked',
                description=f"{request.user.username} liked your post.",
                target_content_type=content_type,
                target_object_id=post.id
            )
        
        return Response({"status": "liked"}, status=status.HTTP_201_CREATED)


class UnlikeView(APIView):
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(user=request.user, post=post)
        
        if like.exists():
            like.delete()
            return Response({"status": "unliked"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "You have not liked this post."},
                status=status.HTTP_400_BAD_REQUEST
            )


class CommentViewSet(viewsets.ModelViewSet):
   
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    
    def perform_create(self, serializer):
        
        comment = serializer.save(author=self.request.user)
        post = comment.post
        user = self.request.user
        
        # Create notification for post author if not the same user
        if post.author != user:
            content_type = ContentType.objects.get_for_model(comment)
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb='commented',
                description=f"{user.username} commented on your post.",
                target_content_type=content_type,
                target_object_id=comment.id
            )
    
    def get_queryset(self):
        
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post', None)
        
        if post_id is not None:
            queryset = queryset.filter(post__id=post_id)
            
        return queryset
            