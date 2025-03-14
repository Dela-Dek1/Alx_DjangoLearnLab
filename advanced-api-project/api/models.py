from django.db import models

# Create your models here.
class Author(models.Model):
    """
    Author model representing a book author.
    
    This model stores basic information about authors and establishes
    a one-to-many relationship with the Book model, allowing an author
    to have multiple books.
    """
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Book model representing a book in the database.
    
    This model stores information about books including title, publication year,
    and establishes a many-to-one relationship with the Author model through
    a foreign key, meaning each book belongs to one author.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='books'
    )
    
    def __str__(self):
        return f"{self.title} ({self.publication_year})"