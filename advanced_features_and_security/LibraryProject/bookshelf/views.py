from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.contenttypes.models import ContentType
from django.views.generic.detail import DetailView
from .models import Library
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Book
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login  
from django.contrib import messages
from django.contrib.auth.models import Group, Permission

def user_has_role(user, roles):
    if not hasattr(user, 'relationship_userprofile'):
        return False
    return user.relationship_userprofile.role in roles

@permission_required('app_name.can_view', raise_exception=True)
def list_books(request):
    book = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': book})

@permission_required('app_name.can_edit', raise_exception=True)
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_list.html', {'books': book})

@permission_required('app_name.can_edit', raise_exception=True)
def book_create(request):
    if not user_has_role(request.user, ['Librarian', 'Admin']):
        return HttpResponseForbidden("You don't have permission to create books")
        
    if request.method == 'POST':
        pass
        '''form = Book(request.POST)
        if form.is_valid():
            book = form.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})'''

@login_required
def book_edit(request, pk):
    if not user_has_role(request.user, ['Librarian', 'Admin']):
        return HttpResponseForbidden("You don't have permission to edit books")
        
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        pass
        '''form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/book_form.html', {'form': form})'''
        

class LibraryDetailView(DetailView):
    model = Library  
    template_name = 'relationship_app/library_detail.html'  
    context_object_name = 'library'


@login_required
def book_delete(request, pk):
    if not user_has_role(request.user, ['Admin']):
        return HttpResponseForbidden("You don't have permission to delete books")
        
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})