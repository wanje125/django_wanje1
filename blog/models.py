from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown #화면에 포스트를 렌더링할때 마크다운 기능이 나타나게 할려면 마크다운 문법으로 
                                        #작성된 content필드값을 html로 변환하는 작업이 필요하다.
import os
# Create your models here.
class Tag(models.Model): #post 위에 추가 해야된다
    name=models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True) #slug는 한글적용이 자동으로 안되서 allow_unicode를 해줘야된다

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/' #f string이란 방법인데 format이랑 똑같다.{}안에 특정 변수를 넣는다.

class Category(models.Model): #post 위에 추가 해야된다
    name=models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/' #f string이란 방법인데 format이랑 똑같다.
    

    class Meta:
        verbose_name_plural='Categories'

class Post(models.Model):
    title=models.CharField(max_length=30, verbose_name='제목')
    content=MarkdownxField()
    hook_text=models.CharField(max_length=100,blank=True, verbose_name='요약문')
    created_at=models.DateTimeField(auto_now_add=True,verbose_name='생성시간')
    updated_at=models.DateTimeField(auto_now=True,verbose_name='변경시간')
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    tags=models.ManyToManyField(Tag, blank=True)


    def __str__(self):
        return f'[{self.pk}{self.title}] :: {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/' #pk는 primary key로 자동으로 생성

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)
    
    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]

    def get_content_markdown(self):
        return markdown(self.content) #마크다운 문법으로 작성된content 모델을 html로 보이게 전환한다.
                                        #템플릿에서 get_content_markdown을 입력해서 적용시킨다.

class Comment(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}' #어드민에서 view on site를 눌리면 해당 댓글을 바로 볼 수 있다. 여기가 잘 이해가 안되긴 하다

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url() #로그인 계정의 아바타 url을 가져온다.
        else:
            return f'https://doitdjango.com/avatar/id/25/818036b33e566bc0/svg/{self.author.email}'
