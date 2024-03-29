from django.shortcuts import render_to_response,redirect,render
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from django.contrib import auth
from django.urls import reverse
import datetime

from read_statistics.utils import get_seven_read_data, get_today_hot_data, get_yesterday_hot_data


from blog.models import Blog

def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days = 7)
    blogs = Blog.objects.filter(read_details__date__lt = today,
                                read_details__date__gte = date) \
                        .values('id', 'title')\
                        .annotate(read_num_sum = Sum('read_details__read_num')) \
                        .order_by('-read_num_sum')
    return blogs[:7]

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_read_data(blog_content_type)
    today_hot_data = get_today_hot_data(blog_content_type)
    yesterday_hot_data = get_yesterday_hot_data(blog_content_type)

    # 获取7天热门博客的缓存数据
    hot_data_for_7_days = cache.get('hot_data_for_7_days')
    if hot_data_for_7_days is None:
        hot_data_for_7_days = get_7_days_hot_blogs()
        cache.set('hot_data_for_7_days', hot_data_for_7_days, 3600)
    #     print('calc')
    # else:
    #     print("use cache")

    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = today_hot_data
    context['yesterday_hot_data'] = yesterday_hot_data
    context['hot_data_for_7_days'] = hot_data_for_7_days # get_7_days_hot_blogs()
    return render_to_response('home.html', context)

def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(request, username = username, password=password)
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    if user is not None:
        auth.login(request, user)
        return redirect(referer)
    else:
        return render(request, 'error.html', {'msg': '用户名或密码不正确'})

def logout(request):
    auth.logout(request)
    return redirect('home')

