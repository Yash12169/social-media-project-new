from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User= get_user_model()
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profilepic = models.FileField(upload_to='images')



    
class profile(models.Model):
    user=models.OneToOneField(User, related_name='profile',on_delete=models.CASCADE)
    discription= models.TextField(default="")
    image= models.ImageField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)



class post(models.Model):
    user=models.ForeignKey(User, related_name='post',on_delete=models.CASCADE)
    discription= models.TextField(default="")
    image= models.ImageField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)



class likepost(models.Model):
    user_id=models.ForeignKey(User,related_name="likepost",on_delete=models.CASCADE)
    post_id=models.ForeignKey(post,related_name="likepost",on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)