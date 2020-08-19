from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.parsers import JSONParser
from .models import Usercart, Uerdet
from .serializers import Userserializer, Userdetailsserializer, Restserial, Usergetdetailsserializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
import json
from rest_framework.response import Response
from datetime import date
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .files import *
# Create your views here.


@api_view(['POST'])
@permission_classes([permissions.AllowAny, ])
def signup_user(request):

    data = {
        'email': request.data['email'],
        'username': request.data['username'],
        'password': request.data['password']
    }
    print(request.data)
    check_user = None
    try:
        check_user = User.objects.filter(email=request.data['email']).first()
    except Exception as e:
        pass
    if check_user == None:
        seril = Userserializer(data=data)
        if seril.is_valid():
            seril.save()
            Userextra(seril.data, request.data)
            # token_genrator(em)

            return Response({'status': 'success'})
        else:
            print(seril.errors)
    else:
        new_seril = User.objects.get(username=check_user)
        dats = Userserializer(new_seril)
        lp = Userextra(dats.data, request.data)
        if lp == True:
            return Response({'status': 'success'})
        else:
            Response({'status': 'error'})
    return Response({'status': 'error'})


@api_view(['GET'])
def user_details(request):
    res = Uerdet.objects.all()
    seril = Usergetdetailsserializer(res, many=True)
    return Response({'data': seril.data})


@api_view(['GET'])
def user_single_details(request):
    user = request.user.id
    usr = Uerdet.objects.get(userid=user)
    print(usr)
    seril = Usergetdetailsserializer(usr)
    print(seril.data)
    return Response({'data': seril.data})


@api_view(['POST'])
@permission_classes([permissions.AllowAny, ])
def checker(request):
    username = None
    usert = 'staff'
    try:
        username = User.objects.get(email=request.data['email'])
        print(username.is_superuser)
        if username.is_superuser:
            usert = 'admin'
    except Exception as e:
        pass
    newuser = None
    try:
        password = request.data['password']
        if username.check_password(password):
            newuser = username
        else:
            newuser = None

    except Exception as e:
        pass

    print(newuser, username)
    if newuser != None and username != None:
        if usert != '':
            refresh = RefreshToken.for_user(username)
            print('hi')
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'status': 'success',
                'usert': usert
            })
        else:
            return Response({'STATUS': 'error'})
    else:
        return Response({'STATUS': 'error'})


@api_view(['POST'])
@permission_classes([permissions.AllowAny, ])
def reset_password(request):
    print('hi')
    check_user = None
    try:
        check_user = User.objects.get(email=request.data['email'])
    except Exception as e:
        pass
    new_seril = User.objects.get(username=check_user)
    dats = Userserializer(new_seril)
    print(dats.data['username'])
    data = {
        'username': dats.data['username'],
        'password': request.data['password']
    }

    print(data)
    if check_user != None:
        seril = Restserial(check_user, data=data)
        if seril.is_valid():
            seril.save()

            return Response({'STATUS': 'sucess'})
        else:
            return Response({'stats': seril.errors})
    else:
        return Response({'STATUS': 'error'})
