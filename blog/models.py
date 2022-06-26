from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta

from user.models import User

# Create your models here.
class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    content = models.TextField(max_length=300)
    category = models.ManyToManyField('Category', through='ArticleCategory')
    posted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    exposure_start_date = models.DateTimeField(default=timezone.now)
    exposure_end_date = models.DateTimeField(default=timezone.now()+timedelta(days=7))

    def __str__(self):
        return f"({self.id}) {self.author}님의 {self.title}"

class Comment(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    content = models.TextField(max_length=100)
    posted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Category(models.Model):
    category = models.CharField(max_length=20)
    
    def __str__(self):
        return f"({self.id}) {self.category}"

class ArticleCategory(models.Model):
    article = models.ForeignKey('Article', on_delete=models.SET_NULL, null=True) 
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True) 