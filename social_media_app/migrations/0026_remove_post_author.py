# Generated by Django 4.1.7 on 2023-10-28 03:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_media_app', '0025_post_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
    ]
