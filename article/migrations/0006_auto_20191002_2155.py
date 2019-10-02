# Generated by Django 2.0 on 2019-10-02 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_article_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='article',
            name='read_num',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
