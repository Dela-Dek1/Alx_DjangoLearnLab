# CRUD Operations Summary

## 1. Create a Book
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)


<QuerySet [<Book: 1984>]>

Book.objects.all()

<QuerySet [<Book: 1984>]>

Book.objects.get(title="1984")

<Book: 1984>

book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

<Book: Nineteen Eighty-Four>

book.delete()
Book.objects.all()  # Should return an empty QuerySet

<QuerySet []>



---

### **Steps to Include Outputs**
1. Run each command in the Django shell (`python manage.py shell`).
2. Copy the actual output from the terminal.
3. Paste it below each command in `CRUD_operations.md`.

Including the output makes it clear that the operations work correctly. íº€
