from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User= get_user_model()
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profilepic = models.ImageField(upload_to='images/')



    
class Profile(models.Model):
    user=models.OneToOneField(User, related_name='profile',on_delete=models.CASCADE)
    discription= models.TextField(default="")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)



class Post(models.Model):
    user=models.ForeignKey(User, related_name='post',on_delete=models.CASCADE)
    discription= models.TextField(default="")
    media= models.FileField(upload_to='media/posts/', blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)



class likepost(models.Model):
    user_id=models.ForeignKey(User,related_name="likepost",on_delete=models.CASCADE)
    post_id=models.ForeignKey(Post,related_name="likepost",on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)