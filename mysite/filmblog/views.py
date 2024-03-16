from django.shortcuts import render

from .models import Question


def index(request):
    return render(request, "filmblog/index.html")

def blog(request):
    return render(request, "filmblog/index.html")