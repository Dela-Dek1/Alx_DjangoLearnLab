from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly




class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow anyone to read, but require auth for other actions


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

# Keep the existing BookList view with updated permissions
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow anyone to read, but require auth for other actions

# Update the BookViewSet with appropriate permissions
class BookViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing book instances.
    Provides all CRUD operations: list, create, retrieve, update, and destroy.
    
    Authentication:
    - Token authentication is required for all operations
    
    Permissions:
    - GET (list and retrieve): Authenticated users can view books
    - POST, PUT, PATCH, DELETE: Only admin users can create, update or delete books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        """
        Custom permissions:
        - List and retrieve actions require the user to be authenticated
        - Create, update, and delete actions require the user to be admin
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]