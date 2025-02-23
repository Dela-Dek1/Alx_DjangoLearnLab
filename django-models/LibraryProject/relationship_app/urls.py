from django.urls import path
from .views import list_books, LibraryDetailView  # Import both views
from .views import admin_view, librarian_view, member_view
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

        # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),

    path('admin-view/', admin_view, name='admin_view'),
    path('librarian-view/', librarian_view, name='librarian_view'),
    path('member-view/', member_view, name='member_view'),

      # Secured URLs
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:pk>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:pk>/', views.delete_book, name='delete_book'),

    # URL pattern for the function-based view (list_books)
    path('books/', list_books, name='list_books'),
    # URL pattern for the class-based view (LibraryDetailView)
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]