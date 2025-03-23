from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Tag

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


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }


class PostForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text="Enter tags separated by commas")
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
    
    def clean_tags(self):
        tag_string = self.cleaned_data.get('tags', '')
        if tag_string:
            tags = [tag.strip() for tag in tag_string.split(',') if tag.strip()]
            return tags
        return []
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if commit:
            instance.save()
            
            # Clear existing tags and add new ones
            instance.tags.clear()
            for tag_name in self.cleaned_data.get('tags', []):
                tag, created = Tag.objects.get_or_create(name=tag_name.lower())
                instance.tags.add(tag)
            
        return instance
        



        

