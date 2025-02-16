book.delete()
print(Book.objects.all()) 

book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Confirm deletion
print(Book.objects.all())  # Should return an empty QuerySet if no books remain
