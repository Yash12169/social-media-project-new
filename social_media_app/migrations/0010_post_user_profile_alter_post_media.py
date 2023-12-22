# Generated by Django 4.1.7 on 2023-10-22 03:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social_media_app', '0009_rename_image_post_media'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='user_profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='post', to='social_media_app.userprofile'),
        ),
        migrations.AlterField(
            model_name='post',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to='media/posts/'),
        ),
    ]