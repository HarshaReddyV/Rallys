from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


# Create your models here.
class User(AbstractUser):
    firstName = models.CharField(max_length= 20, null = True)
    lastName = models.CharField(max_length= 20, null=True)
    pass
  

class Tickers(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(max_length=500, blank=False, default='This is a Product..!')
    bse_code = models.CharField(max_length=20)
    nse_code = models.CharField(max_length=20)

    def __str__(self):
        return (self.title)
    
