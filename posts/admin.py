# posts/admin.py

from django.contrib import admin
from .models import Post, PostCategory, PostSubCategory

# Register your models here.

@admin.register(PostCategory)
class PostCategory(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

@admin.register(PostSubCategory)
class PostSubCategory(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Post)
class Post(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
