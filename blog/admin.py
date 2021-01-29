from django.contrib import admin
from .models import Post, Category, Tag, Comment
from markdownx.admin import MarkdownxModelAdmin # 관리자페이지에서도 마크다운 사용
# Register your models here.
admin.site.register(Post, MarkdownxModelAdmin)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)} #admin에서 카테고리의 name을 생성했을때 자동으로 같은 이름의 slug 생성

admin.site.register(Category, CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)} #admin에서 카테고리의 name을 생성했을때 자동으로 같은 이름의 slug 생성

admin.site.register(Tag,TagAdmin)

admin.site.register(Comment)