from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Category, Tag
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
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

class PostCreate(LoginRequiredMixin,UserPassesTestMixin,CreateView):   #로그인믹신을 먼저 써야된다.
    model=Post
    fields=['title','hook_text','content','head_image','file_upload','category']
    template_name='blog/post_form.html'

    def test_func(self): #스태프 권한이 지정되어야만 글을 쓸 수 있다.
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form): # 로그인을 해야지 글을 쓸 수 있는 기능만들기. authenticated +tag추가
        current_user=self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user #모델에 author을 currentuser로 자동으로 저장한다.
            response=super(PostCreate,self).form_valid(form)

            tags_str=self.request.POST.get('tags_str') #템플릿에서 name이 tags_str인 폼으로 들어온 데이터를 tags_str에 저장한다.
            if tags_str:
                tags_str=tags_str.strip() #앞뒤 공백제거
                tags_str=tags_str.replace(',',';') #,를 ;로 변환
                tags_list=tags_str.split(';') # ;를 기준으로 string을 쪼개서 list에 저장

                for t in tags_list:
                    t=t.strip()
                    tag,is_tag_created=Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug=slugify(t, allow_unicode=True) #unicode로 한글도 가능하게 한다. slug는 원래 한글을 지원하지 않는다.
                        tag.save()
                    self.object.tags.add(tag)
            
            return response
        
        else:
            return redirect('/blog/')

class PostUpdate(LoginRequiredMixin, UpdateView):   #로그인믹신을 먼저 써야된다.
    model=Post
    fields=['title','hook_text','content','head_image','file_upload','category']
    template_name='blog/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):   #방문자가 웹사이트 서버에 get 인지 post로 요청했는지 판단하는 기능
                                                    #만약 방문자가 서버에 get으로 들어오면 포스트를 작성할 수 있는 폼 페이지를 보내준다.
                                                    #반면에 post(버튼)로 들어오면 폼이 유효한지 확인하고 문제가 없으면 데이터베이스에 저장한다.
                                                    #만약 권한이 없는 사용자가 post update를 사용하려고 하면 접근을 못하게 해야된다.
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs): #원래 저장되어있던 tags 불러오기
        context=super(PostUpdate,self).get_context_data()
        if self.object.tags.exists():           #만약에 그 인스턴스(포스트)에 tags가 존재하면
            tags_str_list=list()                
            for t in self.object.tags.all():    
                tags_str_list.append(t.name)    #즉 포스트에서 리스트형태로 저장된 태그스트링을 각각 다시 리스트로 넣는다.
            context['tags_str_default']='; '.join(tags_str_list) #그리고 join으로 ;를 경계로 string으로 합쳐준다.
                                                                #context에 tags_str_default로 채워서 템플릿에 쓸수 있게 반환한다.
        return context

    def form_valid(self, form): # tag 불러오고 저장하기, author은 그전에 저장되어있으므로 바꿀 필요가 없어 그에 관한 코드는 삭제한다.
        response=super(PostUpdate,self).form_valid(form)
        self.object.tags.clear() #포스트에서 가져온 태그들을 모두 삭제한다. 그리고 아래에서 다시 가져온다.

        tags_str=self.request.POST.get('tags_str') #템플릿에서 name이 tags_str인 폼(post)으로 들어온 데이터를 tags_str에 저장한다.
        if tags_str:
            tags_str=tags_str.strip() #앞뒤 공백제거
            tags_str=tags_str.replace(',',';') #,를 ;로 변환
            tags_list=tags_str.split(';') # ;를 기준으로 string을 쪼개서 list에 저장

            for t in tags_list:
                t=t.strip()
                tag,is_tag_created=Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug=slugify(t, allow_unicode=True) #unicode로 한글도 가능하게 한다. slug는 원래 한글을 지원하지 않는다.
                    tag.save()
                self.object.tags.add(tag)
        
        return response
    



