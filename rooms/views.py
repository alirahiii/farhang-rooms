from django.shortcuts import render

from .models import Category, Work


def home(request):
    categories = Category.objects.all()
    latest_works = Work.objects.filter(is_published=True).select_related('category').order_by('-created_at')[:8]
    return render(request, 'rooms/home.html', {
        'categories': categories,
        'latest_works': latest_works,
    })
