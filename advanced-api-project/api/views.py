from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

# Create your views here.
# Book views using generic views for CRUD operations
class BookListView(generics.ListAPIView):
    """
    API view to retrieve a list of all books.
    
    This view allows any user (authenticated or not) to view the list of books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

class BookDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve details of a specific book by ID.
    
    This view allows any user to view the details of a single book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

class BookCreateView(generics.CreateAPIView):
    """
    API view to create a new book.
    
    This view restricts book creation to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookUpdateView(generics.UpdateAPIView):
    """
    API view to update an existing book.
    
    This view restricts book updates to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookDeleteView(generics.DestroyAPIView):
    """
    API view to delete a book.
    
    This view restricts book deletion to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

# Author views
class AuthorListView(generics.ListCreateAPIView):
    """
    API view to list all authors and create new authors.
    
    This view allows anyone to view the list of authors but
    restricts creation to authenticated users.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    
    def get_permissions(self):
        """
        Override to apply different permissions for different methods.
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete an author.
    
    This view allows anyone to view author details but restricts
    updates and deletions to authenticated users.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    
    def get_permissions(self):
        """
        Override to apply different permissions for different methods.
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]