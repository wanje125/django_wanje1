from django.db import models

# Create your models here.
class Post(models.Model):
    title=models.CharField(max_length=30, verbose_name='제목')
    content=models.TextField(verbose_name='내용')
    created_at=models.DateTimeField(auto_now_add=True,verbose_name='생성시간')
    updated_at=models.DateTimeField(auto_now=True,verbose_name='변경시간')

    def __str__(self):
        return f'[{self.pk}{self.title}]'

