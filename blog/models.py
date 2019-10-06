from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import exceptions
from ckeditor_uploader.fields import RichTextUploadingField

class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

class Blog(models.Model):
    title = models.CharField(max_length= 50)
    blog_type = models.ForeignKey(BlogType, on_delete= models.DO_NOTHING)
    # content = models.TextField()
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete= models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add= True)
    last_updated_time = models.DateTimeField(auto_now= True)



    def __str__(self):
        return self.title

    def get_read_num(self):
        try:
            return self.readnum.readed_num
        except exceptions.ObjectDoesNotExist:
            return 0

    class Meta:
        ordering = ('-created_time',)


class ReadNum(models.Model):
    readed_num = models.IntegerField(default=0)
    blog = models.OneToOneField(Blog, on_delete= models.DO_NOTHING)

    # def __str__(self):
    #     return self.readed_num.__str__()