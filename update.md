book.title = "Nineteen Eighty-Four"
book.save()
print(Book.objects.get(id=book.id).title)

book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

# Confirm the update
print(Book.objects.get(id=book.id))  # Should display the updated title
