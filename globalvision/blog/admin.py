from django.contrib import admin
from unfold.admin import ModelAdmin
from django_summernote.admin import SummernoteModelAdmin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(ModelAdmin, SummernoteModelAdmin):
    model_icon = 'article'
    summernote_fields = ('body',)
    list_display = ('title', 'author', 'status', 'is_published', 'created_at')
    list_filter = ('status', 'is_published', 'category')
    search_fields = ('title', 'body')
    readonly_fields = ('created_at',)

    fieldsets = (
        ("Content", {
            "fields": ("title", "author", "category", "body", "cover_image"),
        }),
        ("Publication Details", {
            "fields": ("status", "is_published", "created_at"),
        }),
    )
