from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm
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

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.work = work
            comment.save()
            messages.success(request, 'نظر شما با موفقیت ثبت شد.')
            return redirect('work_detail', slug=work.slug)
    else:
        form = CommentForm()

    comments = work.comments.filter(is_approved=True).order_by('-created_at')
    return render(request, 'rooms/work_detail.html', {
        'work': work,
        'comments': comments,
        'form': form,
    })
