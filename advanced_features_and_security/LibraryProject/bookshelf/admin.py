from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'date_of_birth', 'profile_photo', 'is_staff')
    
  

class BookAdmin(admin.ModelAdmin):
    search_fields = ('title', 'author')
    list_filter = ('publication_year',)

admin.site.register(Book, BookAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
