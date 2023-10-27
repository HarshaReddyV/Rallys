from django.db import models
from home.models import Tickers 
from datetime import datetime
from rallys import settings

class Topic(models.Model):
    title = models.CharField(max_length=70, blank= False, null = False)
    description = models.TextField(max_length= 500, blank= True, null= True)
    parent_ticker = models.ForeignKey(Tickers, on_delete= models.SET_NULL, null= True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, null= True)
    time = models.DateTimeField(default=datetime.now)
    views = models.IntegerField(default = 0)
    comments = models.IntegerField(default= 0)
    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    time = models.DateTimeField(default=datetime.now)
    parent_comment = models.ForeignKey('self', null = True, blank=True, on_delete = models.CASCADE, default = None)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} in topic {self.topic}"