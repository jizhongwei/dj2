# Generated by Django 2.0 on 2019-10-05 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ('-created_time',)},
        ),
    ]
