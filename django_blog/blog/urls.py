from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    PostByTagListView,
    TagListView
)

urlpatterns = [
    # Homepage - Remove duplicate paths
    path('', PostListView.as_view(), name='blog-home'),
    
    # Search functionality
    path('search/', views.search_posts, name='search-posts'),
    
    # Tag-related URLs - Update to use TagPostsView
    path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='tag-posts'),
    path('tags/', TagListView.as_view(), name='blog-tags'),
    

    # User Authentication
    # Note: 'login/' should use auth_views.LoginView, not views.login
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # Blog Post - Remove duplicate post-detail path
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    # Comments (CBV) - Avoid duplicating comment-delete
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment-create'),  
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),  
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    
    # Comments (FBV) - Use either CBV or FBV, not both  
    path('comment/<int:pk>/edit/', views.comment_edit, name='comment-edit'),
]

