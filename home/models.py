from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.core.exceptions import ValidationError
from rallys import settings

# Create your models here.
class User(AbstractUser):
    firstName = models.CharField(max_length= 20, null = True)
    lastName = models.CharField(max_length= 20, null=True)
    email = models.EmailField(blank = False, unique = True)
    pass
  

class Tickers(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(max_length=500, blank=False, default='')
    bseCode = models.CharField(max_length=20)
    nseCode = models.CharField(max_length=20)

    def __str__(self):
        return (self.title)
    

class WatchList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tickers = models.ForeignKey(Tickers, on_delete=models.CASCADE)