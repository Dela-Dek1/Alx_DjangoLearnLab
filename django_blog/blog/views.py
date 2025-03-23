from django.shortcuts import render
from .models import Post

# Create your views here.
def home(request):
    posts = Post.objects.all().order_by('-published_date')
    return render(request, 'blog/home.html', {'posts': posts})