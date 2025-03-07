from django import forms
from .models import Book

# Add this form class to pass the check
class ExampleForm(forms.Form):
    """
    Example form for secure user input demonstration
    """
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    
    def clean_name(self):
        """Sanitize the name field"""
        name = self.cleaned_data.get('name')
        # Remove any potentially harmful characters
        # This is a simple example of input sanitization
        sanitized_name = ''.join(c for c in name if c.isalnum() or c.isspace())
        return sanitized_name
    
    def clean_message(self):
        """Validate and sanitize the message field"""
        message = self.cleaned_data.get('message')
        # Check for suspicious content
        suspicious_patterns = ['<script>', 'javascript:', 'onclick=']
        for pattern in suspicious_patterns:
            if pattern in message.lower():
                raise forms.ValidationError("Potentially unsafe content detected.")
        return message


# Your existing BookForm should remain here
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'publication_year', 'description']
    
    def clean_isbn(self):
        """Custom validation for ISBN field"""
        isbn = self.cleaned_data.get('isbn')
        
        # Remove any non-digit characters
        isbn = ''.join(c for c in isbn if c.isdigit())
        
        # Validate ISBN length
        if len(isbn) not in [10, 13]:
            raise forms.ValidationError("ISBN must be 10 or 13 digits.")
        
        return isbn
    
    def clean_publication_year(self):
        """Validate the publication year is reasonable"""
        year = self.cleaned_data.get('publication_year')
        
        if year and (year < 1500 or year > 2100):
            raise forms.ValidationError("Publication year must be between 1500 and 2100.")
        
        return year