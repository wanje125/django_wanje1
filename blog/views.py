from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category, Tag
# Create your views here.

class PostList(ListView):
    model=Post
    template_name='blog/blog_list.html'
    ordering='-pk'

    def get_context_data(self, **kwargs):
        context = super(PostList,self).get_context_data()
        context['categories']=Category.objects.all()
        context['no_category_post_count']=Post.objects.filter(category=None).count()
        return context

class PostDetail(DetailView):
    model=Post
    template_name='blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetail,self).get_context_data()
        context['categories']=Category.objects.all()
        context['no_category_post_count']=Post.objects.filter(category=None).count()
        return context


def category_page(request, slug): #url에서 slug를 받아온다.
    if slug =='no_category':
        category='미분류'
        post_list=Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list=Post.objects.filter(category=category)
    
    return render(
        request,
        'blog/blog_list.html',
        {
            'post_list':post_list.order_by('-pk'), #pk랑 id 둘다 써도 된다
            'categories':Category.objects.all(),
            'no_category_post_count':Post.objects.filter(category=None).count(),
            'category':category,

        }
    )

def tag_page(request, slug): #url에서 slug를 받아온다.
    tag = Tag.objects.get(slug=slug)
    post_list=tag.post_set.all()

    
    return render(
        request,
        'blog/blog_list.html',
        {
            'post_list':post_list.order_by('-pk'), #pk랑 id 둘다 써도 된다
            'tag':tag,
            'categories':Category.objects.all(),
            'no_category_post_count':Post.objects.filter(category=None).count()
            

        }
    )

