from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework import generics, viewsets
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# Keep the existing BookList view
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Add the new BookViewSet for full CRUD operations
class BookViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing book instances.
    Provides all CRUD operations: list, create, retrieve, update, and destroy.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer