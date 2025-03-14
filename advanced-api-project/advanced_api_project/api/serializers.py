# api/serializers.py
from rest_framework import serializers
from django.utils import timezone
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
    
    def validate_publication_year(self, value):
       
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    
    This serializer handles the Author model and includes a nested representation
    of all books associated with each author. It demonstrates how to handle
    nested relationships in Django REST Framework.
    """
    # Nested serializer for books related to this author
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']