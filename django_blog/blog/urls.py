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
    CommentDeleteView
)

urlpatterns = [
    # Homepage
    path('', views.home, name='home'),
    path('', views.home, name='blog-home'),

    # User Authentication
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('', PostListView.as_view(), name='blog-home'),

    # Blog Post
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),

    # Comments (CBV)
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment-create'),  
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),  
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    

    # Comments (FBV)  
    path('comment/<int:pk>/edit/', views.comment_edit, name='comment-edit'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment-delete'),
]
