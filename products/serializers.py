from rest_framework import serializers
from .models import Product, Soldproduct, Reviews, Cart, Homeedit, Wishlist, Brand, Location
from users.serializers import Userdetailsserializer, Usergetdetailsserializer, Certainserializer


class Productserial(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'brand', 'price', 'category', 'subcategory', 'size',
                  'discription', 'status', 'discount', 'picture', 'specs', 'uploaded_date')


class Soldserializer(serializers.ModelSerializer):
    user_id = Usergetdetailsserializer(read_only=True)

    class Meta:
        model = Soldproduct
        fields = ('id', 'deliverid', 'total', 'delivery_status',
                  'delivery_type', 'user_id', 'odered_date')


class Soldnewserializer(serializers.ModelSerializer):
    class Meta:
        model = Soldproduct
        fields = ('id', 'deliverid', 'total', 'delivery_status',
                  'delivery_type', 'user_id', 'odered_date')


class Reviewserializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ('id', 'review', 'review_reply', 'ratings',
                  'user_id', 'added_date', 'product_id')


class SendreviewSeril(serializers.ModelSerializer):
    user_id = Userdetailsserializer(read_only=True)

    class Meta:
        model = Reviews
        fields = ('id', 'review', 'review_reply', 'ratings',
                  'user_id', 'added_date', 'product_id')


class Cartseril(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id', 'quantity', 'status', 'user_id',
                  'added_date', 'product_id', 'size', 'solid')


class Cartgetseril(serializers.ModelSerializer):
    product_id = Productserial(read_only=True)
    user_id = Userdetailsserializer(read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'quantity', 'status', 'user_id',
                  'added_date', 'product_id', 'size')


class Homeseril(serializers.ModelSerializer):
    class Meta:
        model = Homeedit
        fields = ('id', 'mainheader', 'maintext', 'bottomtext',
                  'picture', 'trend', 'seller', 'feature')


class Wishseril(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('id', 'added_date', 'user_id', 'product_id')


class Getwishseril(serializers.ModelSerializer):
    product_id = Productserial(read_only=True)

    class Meta:
        model = Wishlist
        fields = ('id', 'added_date', 'user_id', 'product_id')


class Brandseril(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'brandname', 'category')


class Locationseril(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'locationname', 'price')
