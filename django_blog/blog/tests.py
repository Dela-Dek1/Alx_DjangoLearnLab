from django.test import TestCase
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment
from taggit.models import Tag

# Create your tests here.
class PostModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post content.',
            author=self.user
        )
        self.post.post_tags.add('django', 'testing')

    def test_post_creation(self):
        """Test that a post can be created with proper attributes"""
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(Post.objects.count(), 1)

    def test_post_string_representation(self):
        """Test the string representation of a post"""
        self.assertEqual(str(self.post), 'Test Post')

    def test_post_tags(self):
        """Test that tags can be added to a post and retrieved"""
        self.assertEqual(self.post.post_tags.count(), 2)
        self.assertTrue('django' in [tag.name for tag in self.post.post_tags.all()])
        self.assertTrue('testing' in [tag.name for tag in self.post.post_tags.all()])

    def test_get_absolute_url(self):
        """Test the absolute URL for a post"""
        self.assertEqual(
            self.post.get_absolute_url(),
            reverse('post-detail', kwargs={'pk': self.post.pk})
        )


class CommentModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post content.',
            author=self.user
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='This is a test comment.'
        )

    def test_comment_creation(self):
        """Test that a comment can be created with proper attributes"""
        self.assertEqual(self.comment.content, 'This is a test comment.')
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(Comment.objects.count(), 1)

    def test_comment_string_representation(self):
        """Test the string representation of a comment"""
        expected = f'Comment by {self.user.username} on {self.post.title}'
        self.assertEqual(str(self.comment), expected)


class TagViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.post1 = Post.objects.create(
            title='Django Tutorial',
            content='This is a tutorial about Django.',
            author=self.user
        )
        self.post2 = Post.objects.create(
            title='Testing in Django',
            content='How to test Django applications.',
            author=self.user
        )
        
        # Add tags to posts
        self.post1.post_tags.add('django', 'tutorial')
        self.post2.post_tags.add('django', 'testing')
        
        # Common tag for both posts
        self.tag = 'django'

    def test_tag_posts_view(self):
        """Test the tag posts view returns posts with the specified tag"""
        response = self.client.get(reverse('tag-posts', kwargs={'tag_name': self.tag}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/tag_posts.html')
        self.assertEqual(len(response.context['posts']), 2)
        
        # Test with a tag that only one post has
        response = self.client.get(reverse('tag-posts', kwargs={'tag_name': 'tutorial'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['posts']), 1)
        self.assertEqual(response.context['posts'][0].title, 'Django Tutorial')

    def test_tag_list_view(self):
        """Test the tag list view shows all tags"""
        response = self.client.get(reverse('blog-tags'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/all_tags.html')
        # Should show all unique tags (django, tutorial, testing)
        self.assertEqual(len(response.context['tags']), 3)


class PostCreateUpdateTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

    def test_create_post_with_tags(self):
        """Test creating a post with tags"""
        response = self.client.post(reverse('post-create'), {
            'title': 'New Test Post',
            'content': 'This is the content of the test post.',
            'post_tags': 'newtag, testing'
        })
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.title, 'New Test Post')
        self.assertEqual(post.post_tags.count(), 2)
        tag_names = [tag.name for tag in post.post_tags.all()]
        self.assertTrue('newtag' in tag_names)
        self.assertTrue('testing' in tag_names)

    def test_update_post_tags(self):
        """Test updating tags on an existing post"""
        post = Post.objects.create(
            title='Original Post',
            content='Original content',
            author=self.user
        )
        post.post_tags.add('original')
        
        response = self.client.post(reverse('post-update', kwargs={'pk': post.pk}), {
            'title': 'Updated Post',
            'content': 'Updated content',
            'post_tags': 'updated, tag'
        })
        
        updated_post = Post.objects.get(pk=post.pk)
        self.assertEqual(updated_post.title, 'Updated Post')
        self.assertEqual(updated_post.post_tags.count(), 2)
        
        tag_names = [tag.name for tag in updated_post.post_tags.all()]
        self.assertTrue('updated' in tag_names)
        self.assertTrue('tag' in tag_names)
        self.assertFalse('original' in tag_names)


class SearchFunctionalityTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Create posts with different content and tags
        self.post1 = Post.objects.create(
            title='Django Framework',
            content='Learn about the Django web framework',
            author=self.user
        )
        self.post1.post_tags.add('django', 'framework')
        
        self.post2 = Post.objects.create(
            title='Python Programming',
            content='Tips for Python programming',
            author=self.user
        )
        self.post2.post_tags.add('python', 'programming')

    def test_search_by_title(self):
        """Test searching posts by title"""
        response = self.client.get(reverse('search-posts') + '?q=django')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['results']), 1)
        self.assertEqual(response.context['results'][0].title, 'Django Framework')

    def test_search_by_content(self):
        """Test searching posts by content"""
        response = self.client.get(reverse('search-posts') + '?q=programming')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['results']), 1)
        self.assertEqual(response.context['results'][0].title, 'Python Programming')

    def test_search_by_tag(self):
        """Test searching posts by tag"""
        response = self.client.get(reverse('search-posts') + '?q=framework')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['results']), 1)
        self.assertEqual(response.context['results'][0].title, 'Django Framework')