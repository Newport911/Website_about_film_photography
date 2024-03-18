from django.shortcuts import render, get_object_or_404

from .models import Question
from .models import Post


def index(request):
    return render(request, "filmblog/index.html")

def blog(request):
    posts = Post.published.all()
    context=[

    ]
    return render(request, "filmblog/index.html", context=context)

def post_list(request):
    posts = Post.published.all()
    return render(request,
	          'filmblog/index.html',
	          {'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
			     status='published',
			     publish__year=year,
			     publish__month=month,
			     publish__day=day)
    return render(request,
		  'filmblog/index.html',
		  {'post': post})