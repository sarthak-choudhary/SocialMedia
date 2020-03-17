from django.db import models
from django.urls import reverse
from django.conf import settings
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='images/', default='images/one.png')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    about = models.CharField(max_length=140,null=True)
    birthdate = models.DateField(null=True)
    follows = models.ManyToManyField('self',symmetrical=False,related_name='followers')
    
    def __str__(self):
        return self.user.username

@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()

@receiver(post_save,sender=User)
def update_profile(sender,instance,**kwargs):
    instance.profile.save()


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=140,null = False)
    author = models.ForeignKey(User,related_name='posts',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField(null =True)

    def __str__(self):
        return f"Post('{self.title}, {self.author}')"

class Comment(models.Model):
    
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey('Post',on_delete=models.CASCADE)
    comment = models.TextField(null=True)
    date_commented = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment('{self.comment}','{self.post}','{self.author}')"
