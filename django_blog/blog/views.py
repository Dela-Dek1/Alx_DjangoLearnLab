from django.shortcuts import render, redirect
from .models import Post
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def home(request):
    posts = Post.objects.all().order_by('-published_date')
    return render(request, 'blog/home.html', {'posts': posts})

def register(request):
    """
    Handle user registration.
    Creates a new user account and logs in the user upon successful registration.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You are now logged in.')
            return redirect('blog-home')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request):
    """
    Display and update user profile.
    Allow authenticated users to view and edit their profile details.
    """
    if request.method == 'POST':
        # Process the form submission for updating user data
        u_form = UserUpdateForm(request.POST, instance=request.user)
        
        if u_form.is_valid():
            u_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        # Display the current user data in the form
        u_form = UserUpdateForm(instance=request.user)
        
    context = {
        'u_form': u_form,
    }
    
    return render(request, 'blog/profile.html', context)