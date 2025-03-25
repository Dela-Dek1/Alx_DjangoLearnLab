from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'get_tags')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'content', 'post_tags__name')
    
    
    def get_tags(self, obj):
        return ", ".join(o.name for o in obj.post_tags.all())
    
    get_tags.short_description = 'Tags'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    list_filter = ('created_at', 'author', 'post')
    search_fields = ('content',)