from django.contrib import messages
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm
from .models import Category, Comment, Work


def home(request):
    categories = Category.objects.all()
    latest_works = Work.objects.filter(is_published=True).select_related('category').order_by('-created_at')[:8]
    return render(request, 'rooms/home.html', {
        'categories': categories,
        'latest_works': latest_works,
    })


def work_detail(request, slug):
    work = get_object_or_404(Work, slug=slug, is_published=True)

    top_form = CommentForm()
    reply_form = None
    reply_target_id = None

    if request.method == 'POST':
        parent_id = request.POST.get('parent_id')
        parent = None
        if parent_id:
            parent = get_object_or_404(work.comments, id=parent_id, parent__isnull=True)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.work = work
            comment.parent = parent
            comment.save()
            messages.success(request, 'نظر شما با موفقیت ثبت شد.')
            return redirect('work_detail', slug=work.slug)

        if parent:
            reply_form = form
            reply_target_id = parent.id
        else:
            top_form = form

    replies = Comment.objects.filter(is_approved=True).order_by('created_at')
    comments = work.comments.filter(is_approved=True, parent__isnull=True) \
        .order_by('-created_at') \
        .prefetch_related(Prefetch('replies', queryset=replies))

    return render(request, 'rooms/work_detail.html', {
        'work': work,
        'comments': comments,
        'top_form': top_form,
        'reply_form': reply_form,
        'reply_target_id': reply_target_id,
    })
