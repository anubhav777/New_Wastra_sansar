from django.db import models
from django.contrib.postgres.fields import JSONField
from datetime import date
from django.utils import timezone
from users.models import Uerdet
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=128)
    brand = models.CharField(max_length=128)
    price = models.IntegerField(blank=True)
    category = models.CharField(max_length=128)
    subcategory = models.CharField(max_length=128)
    size = models.CharField(max_length=128)
    discription = models.CharField(max_length=10000)
    status = models.CharField(max_length=128)
    discount = models.IntegerField(blank=True)
    picture = JSONField(blank=True, default=dict)
    specs = JSONField(blank=True, default=dict)
    uploaded_date = models.DateField(default=timezone.now, blank=True)


class Soldproduct(models.Model):
    deliverid = models.CharField(max_length=128, blank=True)
    total = models.IntegerField(blank=True)
    delivery_status = models.CharField(max_length=128, blank=True)
    delivery_type = models.CharField(max_length=128, blank=True)
    user_id = models.ForeignKey(Uerdet, on_delete=models.CASCADE, blank=True)
    odered_date = models.DateField(default=timezone.now, blank=True)
