from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('<int:pk>/', views.PostViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('<int:pk>/like/', views.PostViewSet.as_view({'post': 'like'})),
    path('<int:pk>/unlike/', views.PostViewSet.as_view({'post': 'unlike'})),
    path('feed/', views.FeedView.as_view(), name='feed'),
    path('<int:post_pk>/comments/', views.CommentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('<int:post_pk>/comments/<int:pk>/', views.CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
]