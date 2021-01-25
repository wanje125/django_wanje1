from django.db import models
from django.contrib.auth.models import User
import os
# Create your models here.
class Tag(models.Model): #post 위에 추가 해야된다
    name=models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/' #f string이란 방법인데 format이랑 똑같다.

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
    content=models.TextField(verbose_name='내용')
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



