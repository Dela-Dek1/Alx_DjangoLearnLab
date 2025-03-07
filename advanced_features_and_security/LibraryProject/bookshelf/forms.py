# bookshelf/forms.py
from django import forms
from .models import Book

class Book(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'publication_year', 'description']
    
    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        
        # Remove any non-digit characters
        isbn = ''.join(c for c in isbn if c.isdigit())
        
        # Validate ISBN length
        if len(isbn) not in [10, 13]:
            raise forms.ValidationError("ISBN must be 10 or 13 digits.")
        
        return isbn
    
    def clean_publication_year(self):
        year = self.cleaned_data.get('publication_year')
        
        if year and (year < 1500 or year > 2100):
            raise forms.ValidationError("Publication year must be between 1500 and 2100.")
        
        return year