from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.CharField(max_length= 100)
    content = models.TextField()
    # created_time = models.DateTimeField(default= timezone.now)
    created_time = models.DateTimeField(auto_now_add= True)
    last_updated_time = models.DateTimeField(auto_now= True)

    author = models.ForeignKey(User, on_delete= models.DO_NOTHING,
                               default= 1)
    is_deleted = models.BooleanField(default= False)
    read_num = models.PositiveIntegerField(default= 0)
    class Meta:
        verbose_name = '博客'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "<article {}>".format(self.title)
