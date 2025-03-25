from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment
# Remove the Tag import since we'll use taggit instead

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']


# Remove the duplicate PostForm class and keep only one version

class PostForm(forms.ModelForm):
    """
    Form for creating and updating blog posts with tag support.
    Uses django-taggit for tag functionality.
    """
    # No need for a custom tags field - taggit handles this
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'post_tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
            'post_tags': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter tags separated by commas'
            }),
        }
        labels = {
            'post_tags': 'Tags',
        }
        help_texts = {
            'post_tags': 'Enter tags separated by commas',
        }
    
    # No need for clean_tags or custom save method - taggit handles this automatically


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Write your comment here...'
            }),
        }



        

