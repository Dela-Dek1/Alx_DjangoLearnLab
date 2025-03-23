from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    """
    Extended user registration form with additional email field.
    Inherits from Django's UserCreationForm and adds email field validation.
    """
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user information.
    Allows users to update their username and email address.
    """
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']