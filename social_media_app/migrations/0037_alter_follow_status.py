# Generated by Django 4.1.7 on 2023-11-04 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_media_app', '0036_remove_userprofile_followers_follow_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='status',
            field=models.CharField(default='none', max_length=10),
        ),
    ]
