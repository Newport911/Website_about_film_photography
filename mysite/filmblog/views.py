from django.shortcuts import render, get_object_or_404

from .models import Post
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.db.models import Q
from taggit.models import Tag


class PostListView(ListView):
    def get(self, request, tag_slug=None):
        object_list = Post.published.all()
        tag = None

        articles = Post.objects.filter(tags__name=tag)

        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            object_list = object_list.filter(tags__in=[tag])
        per_page = 8  # количество постов на странице для пагинации
        paginator = Paginator(object_list, per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            'filmblog/index.html',
            {'page_obj': page_obj, 'tag': tag, 'articles': articles}
        )


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    try:
        prev_post = post.get_previous_by_publish(status='published')
    except Post.DoesNotExist:
        prev_post = None

    try:
        next_post = post.get_next_by_publish(status='published')
    except Post.DoesNotExist:
        next_post = None

    return render(request, 'filmblog/single-standard.html',
                  {'post': post, 'prev_post': prev_post, 'next_post': next_post})


def search_results(request):
    query = request.GET.get('query')
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query)
        )
    else:
        results = []
    return render(request, 'filmblog/search_results.html', {'results': results, 'query': query})
