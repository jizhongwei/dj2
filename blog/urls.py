from django.urls import path

from . import views


urlpatterns = [
    path('<int:blog_pk>/', views.blog_detail, name = 'blog_detail'),
    path('', views.blog_list, name = 'blog_list'),
    path('type/<int:blogs_type_pk>/', views.blogs_with_type, name = 'blogs_with_type'),
]
