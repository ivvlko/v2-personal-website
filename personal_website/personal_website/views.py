from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost
from .forms import BlogPostForm
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')


def portfolio(request):
    return render(request, 'portfolio.html')


def blog(request):
    return render(request, 'blog.html')


def contacts(request):
    return render(request, 'contacts.html')