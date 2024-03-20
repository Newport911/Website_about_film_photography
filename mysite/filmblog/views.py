from django.shortcuts import render, get_object_or_404

from .models import Question
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post




def index(request):
    return render(request, "filmblog/index.html")

def singl_test(request):
    return render(request, "filmblog/single-standard.html")

def blog(request):
    posts = Post.published.all()
    context=[

    ]
    return render(request, "filmblog/index.html", context=context)

class PostListView(ListView):
    def get(self, request):
        object_list = Post.published.all()
        per_page = 1  # количество постов на странице для пагинации
        paginator = Paginator(object_list, per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            'filmblog/index.html',
            {'page_obj': page_obj}
        )

# def post_list(request):
#     posts = Post.published.all()
#     return render(request,
# 	          'filmblog/index.html',
# 	          {'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
			     status='published',
			     publish__year=year,
			     publish__month=month,
			     publish__day=day)
    return render(request,
		  'filmblog/single-standard.html',
		  {'post': post})