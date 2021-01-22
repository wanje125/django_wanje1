from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post
# Create your views here.

class PostList(ListView):
    model=Post
    template_name='blog/index.html'
    ordering='-pk'

class PostDetail(DetailView):
    model=Post
    template_name='single_pages/landing.html'