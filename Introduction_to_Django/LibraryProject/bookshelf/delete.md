Delete the book you created and confirm the deletion by trying to retrieve all books again.

from bookshelf.models import Book
book = Book.objects.all()   
book.delete()
<!-- (1, {'bookshelf.Book': 1}) -->
print(Book.objects.all())          
<!-- <QuerySet []> -->