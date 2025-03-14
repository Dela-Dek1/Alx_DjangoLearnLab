# Advanced API Development with Django REST Framework

This project demonstrates advanced API development techniques using Django REST Framework, including custom serializers, custom views, filtering, searching, ordering, and testing.

## Project Structure

The project consists of a Django application with the following components:

- **Models**: `Author` and `Book` with a one-to-many relationship
- **Serializers**: Custom serializers with validation and nested relationships
- **Views**: Generic views for CRUD operations
- **Filtering**: Implementation of filtering, searching, and ordering
- **Tests**: Comprehensive unit tests for API endpoints

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Alx_DjangoLearnLab.git
   cd Alx_DjangoLearnLab/advanced-api-project
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Book Endpoints
- `GET /api/books/`: List all books (supports filtering, searching, and ordering)
- `GET /api/books/<int:pk>/`: Retrieve a specific book
- `POST /api/books/create/`: Create a new book (authentication required)
- `PUT /api/books/<int:pk>/update/`: Update a book (authentication required)
- `DELETE /api/books/<int:pk>/delete/`: Delete a book (authentication required)

### Author Endpoints
- `GET /api/authors/`: List all authors (supports filtering, searching, and ordering)
- `POST /api/authors/`: Create a new author (authentication required)
- `GET /api/authors/<int:pk>/`: Retrieve a specific author with their books
- `PUT /api/authors/<int:pk>/`: Update an author (authentication required)
- `DELETE /api/authors/<int:pk>/`: Delete an author (authentication required)

## Filtering, Searching, and Ordering

### Filtering
Use query parameters to filter results:
```
/api/books/?author=1
/api/books/?publication_year=2022
```

### Searching
Use the `search` parameter to search across specified fields:
```
/api/books/?search=python
/api/authors/?search=smith
```

### Ordering
Use the `ordering` parameter to sort results:
```
/api/books/?ordering=title
/api/books/?ordering=-publication_year  # Descending order
```

## Running Tests

Run the tests with the following command:
```bash
python manage.py test api
```

This will execute all the test cases defined in `api/test_views.py`.