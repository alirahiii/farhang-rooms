from urllib.parse import urlencode

from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Category, Comment, Work, WorkRequest


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


@admin.register(WorkRequest)
class WorkRequestAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'category', 'status', 'created_at']
    list_filter = ['status']
    ordering = ['-created_at']
    actions = ['create_work_from_request']

    @admin.action(description='ساخت اثر از روی این درخواست')
    def create_work_from_request(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, 'برای این اکشن فقط یک درخواست را انتخاب کنید.', level=messages.ERROR)
            return

        work_request = queryset.first()
        add_url = reverse('admin:rooms_work_add')
        params = urlencode({
            'title': work_request.title,
            'creator': work_request.creator,
            'category': work_request.category_id,
        })
        return HttpResponseRedirect(f'{add_url}?{params}')
