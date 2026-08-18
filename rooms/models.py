from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Work(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='works')
    creator = models.CharField(max_length=200)
    year = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class WorkRequest(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_ADDED = 'added'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'در انتظار'),
        (STATUS_ADDED, 'اضافه شد'),
        (STATUS_REJECTED, 'رد شد'),
    ]

    title = models.CharField('نام اثر', max_length=200)
    creator = models.CharField('نام پدیدآورنده', max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='work_requests', verbose_name='دسته‌بندی')
    description = models.TextField('توضیح', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100)
    body = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author_name}: {self.body[:30]}'
