# Generated by Django 4.1.7 on 2023-10-27 02:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social_media_app', '0021_rename_post_id_comment_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='social_media_app.userprofile'),
        ),
    ]
