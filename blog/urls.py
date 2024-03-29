"""wanje1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('',views.PostList.as_view()),
    path('<int:pk>/',views.PostDetail.as_view()),
    path('category/<str:slug>/',views.category_page),
    path('tag/<str:slug>/',views.tag_page),
    path('create_post/',views.PostCreate.as_view()),
    path('update_post/<int:pk>/',views.PostUpdate.as_view()),
    path('<int:pk>/new_comment/',views.new_comment),
    path('update_comment/<int:pk>/',views.CommentUpdate.as_view()),
    path('delete_comment/<int:pk>/',views.delete_comment),
    path('search/<str:q>/',views.PostSearch.as_view()), #검색어에 해당하는 값을 문자열로 받고 그 값을 q라고 부르겠다는 의미이다.
]
