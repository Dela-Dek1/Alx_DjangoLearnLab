from django.views.generic.detail import DetailView
from .models import Library
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Book
from django.forms import BookForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login  
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Book


def user_has_role(user, roles):
    if not hasattr(user, 'relationship_userprofile'):
        return False
    return user.relationship_userprofile.role in roles

@login_required
def article_list(request):
    articles = Book.objects.all()
    return render(request, 'articles/article_list.html', {'articles': articles})

@login_required
def article_detail(request, pk):
    article = get_object_or_404(Book, pk=pk)
    return render(request, 'articles/article_detail.html', {'article': article})

@login_required
def article_create(request):
    if not user_has_role(request.user, ['Librarian', 'Admin']):
        return HttpResponseForbidden("You don't have permission to create articles")
        
@login_required
def article_edit(request, pk):
    if not user_has_role(request.user, ['Librarian', 'Admin']):
        return HttpResponseForbidden("You don't have permission to edit articles")
 

@login_required
def article_delete(request, pk):
    if not user_has_role(request.user, ['Admin']):
        return HttpResponseForbidden("You don't have permission to delete articles")
        
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  
            login(request, user)  
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('list_books')  
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})



def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")  

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")  

@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")  

@permission_required('relationship_app.can_add_book')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})

# View to edit a book
@permission_required('relationship_app.can_change_book')
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/edit_book.html', {'form': form})

# View to delete a book
@permission_required('relationship_app.can_delete_book')
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})