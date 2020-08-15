from django.db import models
from datetime import  date
from django.contrib.auth.models import User
from django.utils import timezone

class Uerdet(models.Model):
    address=models.CharField(max_length=128)
    state=models.CharField(max_length=128)
    city=models.CharField(max_length=128)
    phone=models.CharField(max_length=128)
    userid=models.ForeignKey(User,on_delete=models.CASCADE)

class Usercart(models.Model):
    quantity=models.CharField(max_length=200)
    status=models.CharField(max_length=200)
    userd=models.ForeignKey(User,on_delete=models.CASCADE)
