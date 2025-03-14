from django.shortcuts import render
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

# Create your views here.
class BookListView(generics.ListAPIView):
    """
    API view to retrieve a list of all books.
    
    This view allows any user (authenticated or not) to view the list of books.
    It includes filtering, searching, and ordering capabilities.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    # Enable filtering, searching, and ordering capabilities
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Filtering options
    filterset_fields = ['title', 'publication_year', 'author']
    
    # Search options
    search_fields = ['title', 'author__name']
    
    # Ordering options
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']  # Default ordering

class BookDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve details of a specific book by ID.
    
    This view allows any user to view the details of a single book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

class BookCreateView(generics.CreateAPIView):
    """
    API view to create a new book.
    
    This view restricts book creation to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BookUpdateView(generics.UpdateAPIView):
    """
    API view to update an existing book.
    
    This view restricts book updates to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BookDeleteView(generics.DestroyAPIView):
    """
    API view to delete a book.
    
    This view restricts book deletion to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

# Author views
class AuthorListView(generics.ListCreateAPIView):
    """
    API view to list all authors and create new authors.
    
    This view allows anyone to view the list of authors but
    restricts creation to authenticated users. It includes
    filtering, searching, and ordering capabilities.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Enable filtering, searching, and ordering capabilities
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Filtering options
    filterset_fields = ['name']
    
    # Search options
    search_fields = ['name', 'books__title']
    
    # Ordering options
    ordering_fields = ['name', 'id']
    ordering = ['name']  # Default ordering

class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete an author.
    
    This view allows anyone to view author details but restricts
    updates and deletions to authenticated users.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]