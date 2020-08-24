from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.contrib.auth.models import User
import json
from rest_framework.response import Response
from datetime import date
from .models import Product, Soldproduct, Reviews, Cart, Homeedit, Wishlist, Brand, Location
from .serializers import Productserial, Soldserializer, Reviewserializer, SendreviewSeril, Soldnewserializer, Cartseril, Cartgetseril, Homeseril, Getwishseril, Wishseril, Brandseril, Locationseril
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from .files import *
from users.models import Uerdet
from users.serializers import Userdetailsserializer
from unique_id import get_unique_id
from django.conf import settings
from django.db.models import Q

bd = os.path.join(settings.BASE_DIR, 'wastrasansar/build/static/img/pembada/')
cd = os.path.join(settings.BASE_DIR, 'wastrasansar/build/static/img/banner/')


@api_view(['POST', 'PUT', 'DELETE'])
def addproduct(request):
    # product_name=request.data['name']
    # print(request.FILES.getlist("file"))
    # print(request.data['category'])
    if request.method == 'POST':
        user = request.user
        if user.is_superuser:
            # fl=request.FILES.getlist("file")
            # fs = FileSystemStorage(location=bd)
            filearr = {}
            # fl=folder_make(request.data['category'])
            # print(fl)
            count = 1

            for f in request.FILES.getlist("file"):
                filename = f.name
                pt = settings.BASE_DIR
                new_pt = f"{pt}\media\{filename}"
                if not allowed_image(f.name):

                    return Response({'status': 'error', 'noty': 'file is not valid'})
                if filename == "":
                    return Response({'status': 'error', 'noty': 'file name is empty'})
                if not file_checker(new_pt):
                    return Response({'status': 'error', 'noty': 'Please provide a different filename'})

                fs = FileSystemStorage(location=bd)
                fs.save(filename, f)

                filearr.update({str(count): filename})
                count += 1

            print(request.data, 'hihi')
            sp = specify(request.data['specification'])
            data = {
                'name': request.data['name'],
                'brand': request.data['brand'],
                'price': request.data['price'],
                'category': request.data['category'],
                'subcategory': request.data['subcategory'],
                'size': request.data['size'],
                'discription': request.data['discription'],
                'status': request.data['status'],
                'discount': request.data['discount'],
                'picture': filearr,
                'specs': sp

            }
            print(data)
            # specify(request.data['specification'])
            # print(request.data['specification'],)

            check = None

            try:
                check = Product.objects.get(name=request.data['name'])
            except:
                pass
            if check == None:
                seril = Productserial(data=data)
                if seril.is_valid():
                    seril.save()
                    return Response({'stats': 'sucess'})
                else:
                    print(seril.errors)
                    return Response({'stats': 'error'})
        else:

            return Response({'status': 'operr'})
    elif request.method == 'PUT':
        # print(request)
        # user=request.user
        # if user.is_superuser:
        # sp=specify(request.data['specification'])
        data = {
            'name': request.data['name'],
            'brand': request.data['brand'],
            'price': request.data['price'],
            'category': request.data['category'],
            'subcategory': request.data['subcategory'],
            'size': request.data['size'],
            'discription': request.data['discription'],
            'status': request.data['status'],
            'discount': request.data['discount'],
            # 'specs':sp

        }
        check = None
        try:
            check = Product.objects.get(id=request.data['id'])
        except:
            pass
        if check != None:
            seril = Productserial(check, data=data)
            if seril.is_valid():
                seril.save()
                return Response({'stats': 'sucess'})
            else:
                print(seril.errors)
                return Response({'stats': 'error'})
        else:
            return Response({'status': 'There is no such product'})
        # else:
        #         print(seril.errors)
        #         return Response({'status':'error'})
    elif request.method == 'DELETE':
        user = request.user
        if user.is_superuser:
            check = Product.objects.get(id=request.META['HTTP_ID'])
            print(request.META['HTTP_ID'])
            check.delete()
            return Response({'status': 'success'})
        else:

            return Response({'status': 'error'})
