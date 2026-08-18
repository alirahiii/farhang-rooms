from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

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

    top_form = CommentForm()
    reply_form = None
    reply_target_id = None

    if request.method == 'POST':
        parent_id = request.POST.get('parent_id')
        parent = None
        if parent_id:
            parent = get_object_or_404(work.comments, id=parent_id)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.work = work
            comment.parent = parent
            comment.save()
            messages.success(request, 'نظر شما با موفقیت ثبت شد.')
            url = reverse('work_detail', kwargs={'slug': work.slug}) + f'#comment-{comment.id}'
            return redirect(url)

        if parent:
            reply_form = form
            reply_target_id = parent.id
        else:
            top_form = form

    comments = _build_comment_threads(work)

    return render(request, 'rooms/work_detail.html', {
        'work': work,
        'comments': comments,
        'top_form': top_form,
        'reply_form': reply_form,
        'reply_target_id': reply_target_id,
    })


def _build_comment_threads(work):
    """Group approved comments by root ancestor, flattening any reply depth to one level."""
    all_comments = list(
        work.comments.filter(is_approved=True).select_related('parent').order_by('created_at')
    )

    roots = []
    threads = {}
    root_of = {}

    for comment in all_comments:
        if comment.parent_id is None:
            roots.append(comment)
            root_of[comment.id] = comment.id
            threads[comment.id] = []
        else:
            root_id = root_of.get(comment.parent_id)
            if root_id is None:
                continue
            root_of[comment.id] = root_id
            threads[root_id].append(comment)

    roots.sort(key=lambda c: c.created_at, reverse=True)
    for comment in roots:
        comment.thread = threads[comment.id]

    return roots
