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


class Reviews(models.Model):
    review = models.CharField(max_length=10000, blank=True)
    review_reply = models.CharField(max_length=10000, blank=True)
    ratings = models.IntegerField(blank=True)
    user_id = models.ForeignKey(Uerdet, on_delete=models.CASCADE, blank=True)
    added_date = models.DateField(default=timezone.now, blank=True)
    product_id = models.ForeignKey(
        'Product', on_delete=models.CASCADE, blank=True)


class Cart(models.Model):
    quantity = models.CharField(max_length=128, blank=True)
    status = models.CharField(max_length=128)
    user_id = models.ForeignKey(Uerdet, on_delete=models.CASCADE, blank=True)
    added_date = models.DateField(default=timezone.now, blank=True)
    size = models.CharField(max_length=128, blank=True)
    product_id = models.ForeignKey(
        'Product', on_delete=models.CASCADE, blank=True)
    solid = models.ForeignKey(
        'Soldproduct', on_delete=models.CASCADE, blank=True, null=True)


class Homeedit(models.Model):
    mainheader = models.CharField(max_length=10000, blank=True)
    maintext = models.CharField(max_length=10000, blank=True)
    bottomtext = models.CharField(max_length=10000, blank=True)
    picture = models.CharField(max_length=10000, blank=True)
    trend = JSONField(blank=True, default=dict)
    seller = JSONField(blank=True, default=dict)
    feature = JSONField(blank=True, default=dict)


class Wishlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    added_date = models.DateField(default=timezone.now, blank=True)
    product_id = models.ForeignKey(
        'Product', on_delete=models.CASCADE, blank=True)


class Brand(models.Model):
    brandname = models.CharField(max_length=10000, blank=True)
    category = models.CharField(max_length=10000, blank=True)


class Location(models.Model):
    locationname = models.CharField(max_length=10000, blank=True)
    price = models.CharField(max_length=10000, blank=True)
