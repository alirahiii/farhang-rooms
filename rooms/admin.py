from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import slugify

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
        for work_request in queryset:
            base_slug = slugify(work_request.title) or f'work-{work_request.id}'
            slug = base_slug
            suffix = 1
            while Work.objects.filter(slug=slug).exists():
                suffix += 1
                slug = f'{base_slug}-{suffix}'

            work = Work.objects.create(
                title=work_request.title,
                slug=slug,
                category=work_request.category,
                creator=work_request.creator,
                description=work_request.description,
                is_published=False,
            )
            work_request.status = WorkRequest.STATUS_ADDED
            work_request.save(update_fields=['status'])

            edit_url = reverse('admin:rooms_work_change', args=[work.id])
            self.message_user(
                request,
                format_html('اثر «{}» ساخته شد. <a href="{}">ویرایش اثر</a>', work.title, edit_url),
            )
