book.title = "Nineteen Eighty-Four"
book.save()
print(Book.objects.get(id=book.id).title)

