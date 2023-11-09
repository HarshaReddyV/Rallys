from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.core.exceptions import ValidationError
from rallys.settings import AUTH_USER_MODEL

# Create your models here.

class Tickers(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(max_length=500, blank=False, default='')
    bseCode = models.CharField(max_length=20)
    nseCode = models.CharField(max_length=20)

    def __str__(self):
        return (self.title)
    
class User(AbstractUser):
    firstName = models.CharField(max_length= 20, null = True)
    lastName = models.CharField(max_length= 20, null=True)
    email = models.EmailField(blank = False, unique = True)
    pass
  
class WatchList(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    stocks = models.ManyToManyField(Tickers, related_name='user_stocks')