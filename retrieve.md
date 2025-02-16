book = Book.objects.get(title="1984")
print(book.title, book.author, book.publication_year)

books = Book.objects.all()
print(books)  # Displays all books in the database

book = Book.objects.get(title="1984")
print(book.title, book.author, book.publication_year)
