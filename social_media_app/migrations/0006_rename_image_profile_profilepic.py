# Generated by Django 4.1.7 on 2023-10-09 02:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_media_app', '0005_alter_userprofile_profilepic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='image',
            new_name='profilepic',
        ),
    ]
