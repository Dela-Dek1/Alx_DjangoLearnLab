from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserUpdateForm, PostForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django import forms
from .forms import CommentForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q, Count
from taggit.models import Tag


# Comment-related Class-Based Views
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs['pk']})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})


# Tag-related Views - New Class-Based Implementation
class TagPostsView(ListView):
    """Class-based view for displaying posts filtered by tag"""
    model = Post
    template_name = 'blog/tag_posts.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        tag_name = self.kwargs.get('tag_name')
        self.tag = get_object_or_404(Tag, name=tag_name)
        return Post.objects.filter(post_tags=self.tag).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        context['title'] = f'Posts tagged with "{self.tag.name}"'
        return context

class TagListView(ListView):
    """Class-based view for displaying all tags"""
    model = Tag
    template_name = 'blog/all_tags.html'
    context_object_name = 'tags'
    
    def get_queryset(self):
        return Tag.objects.annotate(
            num_posts=Count('taggit_taggeditem_items')
        ).order_by('-num_posts')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Browse by Tags'
        return context


# Search Posts View (Updated to include tag search)
def search_posts(request):
    query = request.GET.get('q', '')
    results = Post.objects.none()
    
    if query:
        # Updated to search in title, content, and tags
        results = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(post_tags__name__icontains=query)  # Search in tags
        ).distinct()
    
    context = {
        'query': query,
        'results': results,
        'result_count': results.count()
    }
    return render(request, 'blog/search_results.html', context)


# User Authentication Views
def register(request):
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
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        
    context = {
        'u_form': u_form,
    }
    
    return render(request, 'blog/profile.html', context)


# Remove duplicate home function - use PostListView instead

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-created_at']  # Updated from published_date to created_at
    paginate_by = 5
    
    # Added popular tags to context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_tags'] = Tag.objects.annotate(
            num_posts=Count('taggit_taggeditem_items')
        ).order_by('-num_posts')[:10]
        return context

class PostDetailView(DetailView):
    model = Post
    
    # Enhanced to include related posts by tag
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        # Get related posts by tag
        post_tags_ids = post.post_tags.values_list('id', flat=True)
        similar_posts = Post.objects.filter(post_tags__in=post_tags_ids).exclude(id=post.id).distinct()
        context['similar_posts'] = similar_posts.order_by('-created_at')[:4]
        
        # Add comments
        context['comments'] = post.comments.all().order_by('-created_at')
        context['comment_form'] = CommentForm()
        
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# Comment Form Class (Move this to forms.py)
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write a comment...'}),
        }


# Post Detail Function-Based View (Can be removed if using PostDetailView class)
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('-created_at')
    
    # Added related posts by tag
    post_tags_ids = post.post_tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(post_tags__in=post_tags_ids).exclude(id=post.id).distinct()
    similar_posts = similar_posts.order_by('-created_at')[:4]
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid() and request.user.is_authenticated:
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('post-detail', pk=post.pk)
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'similar_posts': similar_posts,  # Added similar posts
    }
    return render(request, 'blog/post_detail.html', context)


# Comment Management Function-Based Views (Can be removed if using class-based views)
@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    
    if comment.author != request.user:
        messages.error(request, 'You do not have permission to edit this comment.')
        return redirect('post-detail', pk=comment.post.pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your comment has been updated!')
            return redirect('post-detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    
    context = {
        'form': form,
        'comment': comment,
    }
    return render(request, 'blog/comment_edit.html', context)

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    
    if comment.author != request.user:
        messages.error(request, 'You do not have permission to delete this comment.')
        return redirect('post-detail', pk=comment.post.pk)
    
    post_pk = comment.post.pk
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Your comment has been deleted!')
        return redirect('post-detail', pk=post_pk)
    
    context = {
        'comment': comment,
    }
    return render(request, 'blog/comment_confirm_delete.html', context)