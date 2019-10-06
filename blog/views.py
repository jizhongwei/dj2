from django.shortcuts import render, get_object_or_404, render_to_response
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.conf import settings

from read_statistics.models import ReadNum
from .models import Blog, BlogType
from read_statistics.utils import read_statistics_once_read


def blog_list(request):
    blogs_all_list = Blog.objects.all()
    paginator = Paginator(blogs_all_list, settings.NUMBER_BLOGS_PER_PAGE)
    page_num = request.GET.get('page', 1)
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
                 list(range(current_page_num, min(current_page_num + 2, paginator.num_pages)+1))

    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # BlogType.objects.annotate(blog_count = Count('blog'))
    context = {}
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.all()
    context['page_range'] = page_range
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order= 'DESC')
    return render_to_response('blog/blog_list.html', context)


def blog_detail(request, blog_pk):
    context = {}
    blog = get_object_or_404(Blog, pk = blog_pk)
    read_cookie_key = read_statistics_once_read(request, blog)

    context['previous_blog'] = Blog.objects.filter(created_time__gt= blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt= blog.created_time).first()
    context['blog'] = blog
    response =  render_to_response('blog/blog_detail.html', context)
    response.set_cookie(read_cookie_key, 'true', max_age= 60)
    return response

def blogs_with_type(request, blogs_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType, id = blogs_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type= blog_type)
    paginator = Paginator(blogs_all_list, settings.NUMBER_BLOGS_PER_PAGE)
    page_num = request.GET.get('page', 1)
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
                 list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))

    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context['blog_type'] = blog_type
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.all()
    context['page_range'] = page_range
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order= 'DESC')

    return render_to_response('blog/blogs_with_type.html', context)


def blogs_with_date(request, year, month):
    context = {}

    blogs_all_list = Blog.objects.filter(created_time__year= year,
                                         created_time__month= month)
    paginator = Paginator(blogs_all_list, settings.NUMBER_BLOGS_PER_PAGE)
    page_num = request.GET.get('page', 1)
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
                 list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))

    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context['blogs_with_date'] = '{}年{}月'.format(year, month)
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.all()
    context['page_range'] = page_range
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order= 'DESC')

    return render_to_response('blog/blogs_with_date.html', context)