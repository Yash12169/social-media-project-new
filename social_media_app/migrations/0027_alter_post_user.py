# Generated by Django 4.1.7 on 2023-10-28 03:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social_media_app', '0026_remove_post_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='social_media_app.userprofile'),
        ),
    ]
