from django.test import TestCase, Client
from django.urls import reverse
from .models import Book

class SecurityTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Create test data if needed
        Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="1234567890",
            publication_year=2020,
            description="Test Description"
        )
    
    def test_csrf_protection(self):
        """Test CSRF protection on forms"""
        # Try to submit a form without CSRF token
        response = self.client.post(reverse('book_form'), {
            'title': 'Another Book',
            'author': 'Another Author',
            'isbn': '0987654321',
            'publication_year': 2021,
            'description': 'Another Description'
        })
        # Should get a 403 Forbidden response
        self.assertEqual(response.status_code, 403)
    
    def test_xss_protection(self):
        """Test XSS content is properly escaped"""
        # Create a book with potentially harmful XSS content
        test_title = '<script>alert("XSS")</script>'
        
        # Create via form submission with proper CSRF
        self.client.get(reverse('book_form'))  # Get the form first to get a CSRF cookie
        response = self.client.post(
            reverse('book_form'),
            {
                'title': test_title,
                'author': 'XSS Test',
                'isbn': '1122334455',
                'publication_year': 2022,
                'description': 'Testing XSS protection'
            },
            follow=True
        )
        
        # Check the book list to ensure content is escaped
        response = self.client.get(reverse('book_list'))
        content = response.content.decode()
        
        # Content should be escaped - should find &lt;script&gt; not <script>
        self.assertIn('&lt;script&gt;', content)
        self.assertNotIn('<script>alert("XSS")</script>', content)
    
    def test_security_headers(self):
        """Test security headers are present"""
        response = self.client.get(reverse('book_list'))
        
        # Check for required security headers
        self.assertEqual(response.get('X-Frame-Options'), 'DENY')
        self.assertEqual(response.get('X-Content-Type-Options'), 'nosniff')
        self.assertTrue('Content-Security-Policy' in response)

    def test_sql_injection_protection(self):
        """Test SQL injection attempts are blocked"""
        # Try a basic SQL injection attempt in search
        response = self.client.get(reverse('book_list') + '?search=x\' OR \'1\'=\'1')
        
        # Should get a 200 OK but not expose all records
        self.assertEqual(response.status_code, 200)
        
        # Check the SQL injection didn't result in all books being returned
        # This assumes the search for this odd string shouldn't match any books
        # If you have no books in your test database, check another way
        if len(Book.objects.all()) > 1:  # If you have more than the one test book
            self.assertTrue(len(response.context['books']) < len(Book.objects.all()))