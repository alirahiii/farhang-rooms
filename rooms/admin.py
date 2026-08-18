from django.contrib import admin

from .models import Category, Comment, Work


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_filter = ['category']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_filter = ['is_approved']
