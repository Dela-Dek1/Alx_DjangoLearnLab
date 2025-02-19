Retrieve and display all attributes of the book you just created.

book = Book.objects.get(title="1984")
print(book.title, book.author, book.publication_year)

<!-- <QuerySet [{'id': 1, 'title': '1984', 'author': 'George Orwell', 'publication_year': 1949}] -->