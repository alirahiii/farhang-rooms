from django.shortcuts import get_object_or_404, render

from .models import Category, Work


def home(request):
    categories = Category.objects.all()
    latest_works = Work.objects.filter(is_published=True).select_related('category').order_by('-created_at')[:8]
    return render(request, 'rooms/home.html', {
        'categories': categories,
        'latest_works': latest_works,
    })


def work_detail(request, slug):
    work = get_object_or_404(Work, slug=slug, is_published=True)
    comments = work.comments.filter(is_approved=True).order_by('-created_at')
    return render(request, 'rooms/work_detail.html', {
        'work': work,
        'comments': comments,
    })
