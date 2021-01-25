from django.contrib import admin
from .models import Post, Category, Tag
# Register your models here.
admin.site.register(Post)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)} #admin에서 카테고리의 name을 생성했을때 자동으로 같은 이름의 slug 생성

admin.site.register(Category, CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)} #admin에서 카테고리의 name을 생성했을때 자동으로 같은 이름의 slug 생성

admin.site.register(Tag,TagAdmin)