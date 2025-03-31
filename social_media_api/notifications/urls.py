# Create notifications/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification-list'),
    path('<int:notification_id>/mark-read/', views.MarkNotificationReadView.as_view(), name='mark-notification-read'),
    path('mark-all-read/', views.MarkAllNotificationsReadView.as_view(), name='mark-all-notifications-read'),
]