from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User= get_user_model()

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profilepic = models.ImageField(upload_to='images/')
    discription = models.CharField(max_length=1000,default="")


class Post(models.Model):
    user=models.ForeignKey(User, related_name='post',on_delete=models.CASCADE)
    discription= models.TextField(default="")
    media= models.FileField(upload_to='media/posts/', blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    likes_count=models.PositiveIntegerField(default=0)
    comment_count=models.IntegerField(default=0)
    
class Profile(models.Model):
    user=models.OneToOneField(User, related_name='profile',on_delete=models.CASCADE)
    discription= models.TextField(default="")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)

class LikePost(models.Model):
    user=models.ForeignKey(User,related_name="likepost",on_delete=models.CASCADE)
    post=models.ForeignKey(Post,related_name="likepost",on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)


class Comment(models.Model):
    post=models.ForeignKey(Post,related_name='comment', on_delete=models.CASCADE)
    author= models.ForeignKey(UserProfile,related_name='comment',on_delete=models.CASCADE)
    text=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

class Follow(models.Model):
    follower=models.ForeignKey(User,related_name='follower',on_delete=models.CASCADE)
    following=models.ForeignKey(User,related_name='following',on_delete=models.CASCADE)
    status= models.CharField(max_length=10,default='none')

