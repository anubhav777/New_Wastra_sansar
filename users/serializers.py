from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from .models import Usercart, Uerdet


class Userserializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[
                                   UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(required=True, validators=[
                                     UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class Certainserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')


class Restserial(serializers.ModelSerializer):

    username = serializers.CharField(required=True, validators=[
                                     UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        user = User.objects.update_or_create(
            validated_data['username'], validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')


class Userdetailsserializer(serializers.ModelSerializer):
    userid = Certainserializer(read_only=True)

    class Meta:
        model = Uerdet
        fields = ('id', 'address', 'state', 'city', 'phone', 'userid')


class Usersecserializer(serializers.ModelSerializer):

    class Meta:
        model = Uerdet
        fields = ('id', 'address', 'state', 'city', 'phone', 'userid')


class Usergetdetailsserializer(serializers.ModelSerializer):
    userid = Certainserializer(read_only=True)

    class Meta:
        model = Uerdet
        fields = ('id', 'address', 'state', 'city', 'phone', 'userid')
