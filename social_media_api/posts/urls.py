from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView, LikeView, UnlikeView

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

app_name = 'posts'

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedView.as_view(), name='feed'),
    path('posts/feed/', PostViewSet.as_view({'get': 'feed'}), name='posts-feed'),
    path('posts/<int:pk>/like/', LikeView.as_view(), name='like-post'),
    path('posts/<int:pk>/unlike/', UnlikeView.as_view(), name='unlike-post'),
]
