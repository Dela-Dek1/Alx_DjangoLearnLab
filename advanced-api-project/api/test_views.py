from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Author, Book



class BookAPITests(APITestCase):
    """Test suite for Book API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpassword123'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name='Author One')
        self.author2 = Author.objects.create(name='Author Two')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Book One',
            publication_year=2020,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='Book Two',
            publication_year=2021,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title='Another Book',
            publication_year=2022,
            author=self.author2
        )
        
        # Configure API client
        self.client = APIClient()
    
    def test_list_books(self):
        """Test getting a list of books."""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_get_book_detail(self):
        """Test getting details of a specific book."""
        response = self.client.get(f'/api/books/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Book One')
    
    def test_create_book_unauthenticated(self):
        """Test creating a book without authentication (should fail)."""
        new_book = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', new_book, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_book_authenticated(self):
        """Test creating a book with authentication."""
        # Use client.login() instead of force_authenticate
        login_successful = self.client.login(username='testuser', password='testpassword123')
        self.assertTrue(login_successful)
        
        new_book = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', new_book, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Book')
    
    def test_update_book_authenticated(self):
        """Test updating a book with authentication."""
        # Use client.login() instead of force_authenticate
        login_successful = self.client.login(username='testuser', password='testpassword123')
        self.assertTrue(login_successful)
        
        updated_data = {
            'title': 'Updated Book One',
            'publication_year': 2020,
            'author': self.author1.id
        }
        response = self.client.put(
            f'/api/books/{self.book1.id}/update/', 
            updated_data, 
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Book One')
    
    def test_delete_book_authenticated(self):
        """Test deleting a book with authentication."""
        # Use client.login() instead of force_authenticate
        login_successful = self.client.login(username='testuser', password='testpassword123')
        self.assertTrue(login_successful)
        
        response = self.client.delete(f'/api/books/{self.book1.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())
    
    def test_validation_future_year(self):
        """Test validation error when publication year is in the future."""
        # Use client.login() instead of force_authenticate
        login_successful = self.client.login(username='testuser', password='testpassword123')
        self.assertTrue(login_successful)
        
        future_year = timezone.now().year + 1
        new_book = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', new_book, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_filtering_books(self):
        """Test filtering books by author."""
        response = self.client.get(f'/api/books/?author={self.author1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # author1 has 2 books
    
    def test_searching_books(self):
        """Test searching for books."""
        response = self.client.get('/api/books/?search=Another')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only book3 has 'Another' in the title
    
    def test_ordering_books(self):
        """Test ordering books by title."""
        response = self.client.get('/api/books/?ordering=title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if books are ordered by title (alphabetically)
        self.assertEqual(response.data[0]['title'], 'Another Book')
        self.assertEqual(response.data[1]['title'], 'Book One')
        self.assertEqual(response.data[2]['title'], 'Book Two')

class AuthorAPITests(APITestCase):
    """Test suite for Author API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpassword123'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name='Author One')
        self.author2 = Author.objects.create(name='Author Two')
        
        # Create test books
        Book.objects.create(
            title='Book One',
            publication_year=2020,
            author=self.author1
        )
        Book.objects.create(
            title='Book Two',
            publication_year=2021,
            author=self.author1
        )
        
        # Configure API client
        self.client = APIClient()
    
    def test_list_authors(self):
        """Test getting a list of authors."""
        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_get_author_detail(self):
        """Test getting author details including nested books."""
        response = self.client.get(f'/api/authors/{self.author1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Author One')
        self.assertEqual(len(response.data['books']), 2)  # author1 has 2 books
    
    def test_create_author_authenticated(self):
        """Test creating an author with authentication."""
        # Use client.login() instead of force_authenticate
        login_successful = self.client.login(username='testuser', password='testpassword123')
        self.assertTrue(login_successful)
        
        new_author = {'name': 'New Author'}
        response = self.client.post('/api/authors/', new_author, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Author')
    
    def test_create_author_unauthenticated(self):
        """Test creating an author without authentication (should fail)."""
        new_author = {'name': 'New Author'}
        response = self.client.post('/api/authors/', new_author, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_searching_authors(self):
        """Test searching for authors by name."""
        response = self.client.get('/api/authors/?search=One')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only author1 has 'One' in the name
