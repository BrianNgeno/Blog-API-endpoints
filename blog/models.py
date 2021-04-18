from django.db import models
from datetime import datetime
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



# Create your models here.
# class User(AbstractUser):
#     username = models.CharField(max_length=200, unique=True)
#     email = models.EmailField(max_length=254, unique=True)

    
class Blog(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    time_created = models.DateField(auto_now_add=True)
    publisher = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    content =  models.TextField()
    image = models.ImageField()
    
    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return self.title
    