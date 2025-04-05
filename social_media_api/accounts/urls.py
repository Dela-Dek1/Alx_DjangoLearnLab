# accounts/urls.py

from django.urls import path
from .views import CreateUserView, CreateTokenView, ManageUserView

app_name = 'accounts'

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('login/', CreateTokenView.as_view(), name='login'),
    path('profile/', ManageUserView.as_view(), name='profile'),
]
