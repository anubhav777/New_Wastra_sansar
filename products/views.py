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


@api_view(['GET'])
@permission_classes([permissions.AllowAny, ])
def getproduct(request):
    all_prod = Product.objects.all()
    result = Productserial(all_prod, many=True)
    return Response({'data': result.data})


@api_view(['GET'])
@permission_classes([permissions.AllowAny, ])
def getfiltproduct(request):
    status = request.META['HTTP_STATUS']
    discount = request.META['HTTP_DISCOUNT']
    price = request.META['HTTP_PRICE']
    category = request.META['HTTP_CATEGORY']
    search = request.META['HTTP_SEARCH']
    # print(status,discount,price,category)
    # all_prod=Product.objects.filter(price__range=(1000,2000))

    all_prod = None
    if price != 'Default' and category != 'Default' and status != 'Default' and discount != 'Default':
        if ">" in price:
            newprice = price.split(">")
            newpt = int(newprice[1])
            print(newpt)
            print(category)
            if discount == "discount":
                all_prod = Product.objects.filter(
                    price__gte=newpt, category=category, status=status, discount__gte=1)
            else:
                all_prod = Product.objects.filter(
                    price__gte=newpt, category=category, status=status, discount=0)
        elif "<" in price:
            newprice = price.split("<")
            newpt = int(newprice[1])
            if discount == "discount":
                all_prod = Product.objects.filter(
                    price__lte=newpt, category=category, status=status, discount__gte=1)
            else:
                all_prod = Product.objects.filter(
                    price__lte=newpt, category=category, status=status, discount=0)
        elif "-" in price:
            newprice = price.split("-", 2)
            small = int(newprice[0])
            big = int(newprice[1])
            print(big)
            if discount == "discount":
                all_prod = Product.objects.filter(price__range=(
                    small, big), category=category, status=status, discount__gte=1)
            else:
                all_prod = Product.objects.filter(price__range=(
                    small, big), category=category, status=status, discount=0)
    elif price != 'Default' and category != 'Default' and status != 'Default':
        if ">" in price:
            newprice = price.split(">")
            newpt = int(newprice[1])
            print(newpt)
            print(category)

            all_prod = Product.objects.filter(
                price__gte=newpt, category=category, status=status)

        elif "<" in price:
            newprice = price.split("<")
            newpt = int(newprice[1])
            all_prod = Product.objects.filter(
                price__lte=newpt, category=category, status=status)

        elif "-" in price:
            newprice = price.split("-", 2)
            small = int(newprice[0])
            big = int(newprice[1])
            print(big)
            all_prod = Product.objects.filter(price__range=(
                small, big), category=category, status=status)

    elif price != 'Default' and category != 'Default' and discount != 'Default':
        if ">" in price:
            newprice = price.split(">")
            newpt = int(newprice[1])
            print(newpt)
            print(category)
            if discount == "discount":
                all_prod = Product.objects.filter(
                    price__gte=newpt, category=category, discount__gte=1)
            else:
                all_prod = Product.objects.filter(
                    price__gte=newpt, category=category, discount=0)
        elif "<" in price:
            newprice = price.split("<")
            newpt = int(newprice[1])
            if discount == "discount":
                all_prod = Product.objects.filter(
                    price__lte=newpt, category=category, discount__gte=1)
            else:
                all_prod = Product.objects.filter(
                    price__lte=newpt, category=category, discount=0)
        elif "-" in price:
            newprice = price.split("-", 2)
            small = int(newprice[0])
            big = int(newprice[1])
            print(big)
            if discount == "discount":
                all_prod = Product.objects.filter(price__range=(
                    small, big), category=category, discount__gte=1)
            else:
                all_prod = Product.objects.filter(price__range=(
                    small, big), category=category, discount=0)
    elif price != 'Default' and status != 'Default' and discount != 'Default':
        if ">" in price:
            newprice = price.split(">")
            newpt = int(newprice[1])
            print(newpt)
            print(category)
            if discount == "discount":
                all_prod = Product.objects.filter(
                    price__gte=newpt, status=status, discount__gte=1)
            else:
                all_prod = Product.objects.filter(
                    price__gte=newpt, status=status, discount=0)
        elif "<" in price:
            newprice = price.split("<")
            newpt = int(newprice[1])
            if discount == "discount":
                all_prod = Product.objects.filter(
                    price__lte=newpt, status=status, discount__gte=1)
            else:
                all_prod = Product.objects.filter(
                    price__lte=newpt, status=status, discount=0)
        elif "-" in price:
            newprice = price.split("-", 2)
            small = int(newprice[0])
            big = int(newprice[1])
            print(big)
            if discount == "discount":
                all_prod = Product.objects.filter(price__range=(
                    small, big), status=status, discount__gte=1)
            else:
                all_prod = Product.objects.filter(
                    price__range=(small, big), status=status, discount=0)
    elif category != 'Default' and status != 'Default' and discount != 'Default':
        if discount == "discount":
            all_prod = Product.objects.filter(
                category=category, status=status, discount__gte=1)
        else:
            all_prod = Product.objects.filter(
                category=category, status=status, discount=0)
    elif price != 'Default' and category != 'Default':
        if ">" in price:
            newprice = price.split(">")
            newpt = int(newprice[1])
            print(newpt)
            print(category)

            all_prod = Product.objects.filter(
                price__gte=newpt, category=category)

        elif "<" in price:
            newprice = price.split("<")
            newpt = int(newprice[1])
            all_prod = Product.objects.filter(
                price__lte=newpt, category=category)

        elif "-" in price:
            newprice = price.split("-", 2)
            small = int(newprice[0])
            big = int(newprice[1])
            print(big)
            all_prod = Product.objects.filter(
                price__range=(small, big), category=category)
    elif price != 'Default' and status != 'Default':
        if ">" in price:
            newprice = price.split(">")
            newpt = int(newprice[1])
            print(newpt)
            print(category)

            all_prod = Product.objects.filter(price__gte=newpt, status=status)

        elif "<" in price:
            newprice = price.split("<")
            newpt = int(newprice[1])
            all_prod = Product.objects.filter(price__lte=newpt, status=status)

        elif "-" in price:
            newprice = price.split("-", 2)
            small = int(newprice[0])
            big = int(newprice[1])
            print(big)
            all_prod = Product.objects.filter(
                price__range=(small, big), status=status)
    elif price != 'Default' and discount != 'Default':
        if ">" in price:
            newprice = price.split(">")
            newpt = int(newprice[1])
            print(newpt)
            print(category)
            if discount == "discount":
                all_prod = Product.objects.filter(
                    price__gte=newpt, discount__gte=1)
            else:
                all_prod = Product.objects.filter(price__gte=newpt, discount=0)
        elif "<" in price:
            newprice = price.split("<")
            newpt = int(newprice[1])
            if discount == "discount":
                all_prod = Product.objects.filter(
                    price__lte=newpt, discount__gte=1)
            else:
                all_prod = Product.objects.filter(price__lte=newpt, discount=0)
        elif "-" in price:
            newprice = price.split("-", 2)
            small = int(newprice[0])
            big = int(newprice[1])
            print(big)
            if discount == "discount":
                all_prod = Product.objects.filter(
                    price__range=(small, big), discount__gte=1)
            else:
                all_prod = Product.objects.filter(
                    price__range=(small, big), discount=0)
    elif status != 'Default' and discount != 'Default':
        if discount == "discount":
            all_prod = Product.objects.filter(status=status, discount__gte=1)
        else:
            all_prod = Product.objects.filter(status=status, discount=0)
    elif category != 'Default' and discount != 'Default':
        if discount == "discount":
            all_prod = Product.objects.filter(
                category=category, discount__gte=1)
        else:
            all_prod = Product.objects.filter(category=category, discount=0)
    elif category != 'Default' and status != 'Default':
        all_prod = Product.objects.filter(category=category, status=status)
    elif category != 'Default':
        all_prod = Product.objects.filter(category=category)
    elif status != 'Default':
        all_prod = Product.objects.filter(status=status)
    elif discount != 'Default':
        if discount == "discount":
            all_prod = Product.objects.filter(discount__gte=1)
        else:
            all_prod = Product.objects.filter(discount=0)
    elif price != 'Default':
        if ">" in price:
            newprice = price.split(">")
            newpt = int(newprice[1])
            print(newpt)
            print(category)

            all_prod = Product.objects.filter(price__gte=newpt)

        elif "<" in price:
            newprice = price.split("<")
            newpt = int(newprice[1])
            all_prod = Product.objects.filter(price__lte=newpt)

        elif "-" in price:
            newprice = price.split("-", 2)
            small = int(newprice[0])
            big = int(newprice[1])
            print(big)
            all_prod = Product.objects.filter(price__range=(small, big))
    else:
        all_prod = Product.objects.all()

    result = Productserial(all_prod, many=True)
    return Response({'status': 'done', 'data': result.data})


@api_view(['POST', 'GET', "PUT", "DELETE"])
def wishreq(request):
    if request.method == "POST":
        user = request.user.id
        data = {
            'user_id': user,
            'product_id': request.data['productid']
        }
        check = None
        try:
            check = Wishlist.objects.get(
                user_id=user, product_id=request.data['productid'])
        except:
            pass
        print(check)
        if check == None:
            seril = Wishseril(data=data)
            if seril.is_valid():
                seril.save()
                return Response({'status': 'sucess'})
            else:
                print(seril.errors)
                return Response({'status': 'failed'})
        else:
            return Response({'status': 'already added'})
    elif request.method == "GET":
        user = request.user.id
        dat = Wishlist.objects.filter(user_id=user).all()
        seril = Getwishseril(dat, many=True)
        return Response({'data': seril.data})
    elif request.method == "DELETE":
        print(request.META['HTTP_ID'])
        check = Wishlist.objects.get(id=request.META['HTTP_ID'])

        check.delete()
        return Response({'status': 'success'})


@api_view(['POST', 'GET', "PUT", "DELETE"])
@permission_classes([permissions.AllowAny, ])
def brandat(request):
    if request.method == "POST":
        user = request.user
        if user.is_superuser:
            seril = Brandseril(data=request.data)
            if seril.is_valid():
                seril.save()
                return Response({'status': 'sucess'})
            else:
                print(seril.errors)
                return Response({'staus': 'fail'})
        else:

            return Response({'status': 'error'})
    elif request.method == "GET":
        status = request.META['HTTP_STATUS']
        print(status)
        if status != 'Default':
            dat = Brand.objects.filter(category=status)
            print(dat)
            seril = Brandseril(dat, many=True)
            return Response({'data': seril.data})
        else:
            dat = Brand.objects.all()
            seril = Brandseril(dat, many=True)
            return Response({'data': seril.data})
    elif request.method == "DELETE":
        user = request.user
        if user.is_superuser:
            check = Brand.objects.get(id=request.META['HTTP_ID'])
            print(request.META['HTTP_ID'])
            check.delete()
            return Response({'status': 'success'})
        else:

            return Response({'status': 'error'})


@api_view(['POST', 'GET', "PUT", "DELETE"])
@permission_classes([permissions.AllowAny, ])
def locdat(request):
    if request.method == "POST":
        user = request.user
        if user.is_superuser:
            seril = Locationseril(data=request.data)
            if seril.is_valid():
                seril.save()
                return Response({'status': 'sucess'})
            else:
                print(seril.errors)
                return Response({'staus': 'fail'})
        else:

            return Response({'status': 'error'})
    elif request.method == "GET":
        status = request.META['HTTP_STATUS']
        print(status)
        if status != 'Default':
            dat = Location.objects.filter(locationname=status)
            print(dat)
            seril = Locationseril(dat, many=True)
            return Response({'data': seril.data})
        else:
            dat = Location.objects.all()
            seril = Locationseril(dat, many=True)
            return Response({'data': seril.data})
    elif request.method == "DELETE":
        user = request.user
        if user.is_superuser:
            check = Location.objects.get(id=request.META['HTTP_ID'])
            print(request.META['HTTP_ID'])
            check.delete()
            return Response({'status': 'success'})
        else:
            return Response({'status': 'failed'})


@api_view(['POST', 'GET', "PUT"])
@permission_classes([permissions.AllowAny, ])
def homeset(request):

    if request.method == "POST":
        user = request.user
        if user.is_superuser:
            print(request.data)
            seril = Homeseril(data=request.data)
            if seril.is_valid():
                seril.save()
                return Response({'status': 'sucess'})
            else:
                print(seril.errors)
                return Response({'staus': 'fail'})

        else:

            return Response({'status': 'error'})
    elif request.method == "GET":
        print(bd)
        dat = Homeedit.objects.all()
        seril = Homeseril(dat, many=True)
        return Response({'data': seril.data})
    elif request.method == "PUT":
        user = request.user
        if user.is_superuser:
            data = None
            if request.content_type == 'application/json':
                data = {
                    "mainheader": request.data['mainheader'],
                    "maintext": request.data['maintext'],
                    "bottomtext": request.data['bottomtext'],
                    "picture": request.data['picture'],
                }
            else:
                fl = request.FILES["file"]
                filename = fl.name
                fs = FileSystemStorage(location=cd)
                fs.save(fl.name, fl)
                data = {
                    "mainheader": request.data['mainheader'],
                    "maintext": request.data['maintext'],
                    "bottomtext": request.data['bottomtext'],
                    "picture": filename,
                }
            check = Homeedit.objects.get(id=1)
            seril = Homeseril(check, data)
            if seril.is_valid():
                seril.save()
                return Response({'status': 'success'})
            else:
                print(seril.errors)
                return Response({'status': 'error'})
        else:

            return Response({'status': 'error'})

        # return Response({'status':'success'})
        # fs = FileSystemStorage()
        # filearr={}
        # # fl=folder_make(request.data['category'])
        # # print(fl)
        # count=1

        # for f in request.FILES.getlist("file"):
        #     filename = f.name
        #     pt=settings.BASE_DIR
        #     new_pt=f"{pt}\media\{filename}"
        #     if not allowed_image(f.name):

        #         return Response({'status':'error','noty':'file is not valid'})
        #     if filename == "":
        #         return Response({'status':'error','noty':'file name is empty'})
        #     if not file_checker(new_pt):
        #         return Response({'status':'error','noty':'Please provide a different filename'})

        #     fs = FileSystemStorage()
        #     # flsave=fs.save(filename, f)

        #     filearr.update({str(count):filename})
        #     count+=1


@api_view(['POST', "GET", "PUT"])
def soldprod(request):

    if request.method == "POST":

        user = request.user.id
        em = request.user.email
        usr = Uerdet.objects.get(userid=user)
        # print(request.data['products'])

        check = None
        try:
            check = Soldproduct.objects.get(
                user_id=usr.id, delivery_status='Undelivered')
            # print(check)
        except:
            pass
        # print(check)
        if check == None:
            pro = request.data['products']
            data = {
                'deliverid': get_unique_id(length=15), 'total': request.data['total'], 'delivery_status': 'Undelivered', 'delivery_type': 'Delivery_pay', 'user_id': usr.id, 'odered_date': date.today()
            }
            seril = Soldnewserializer(data=data)
            if seril.is_valid():
                seril.save()
                newproducts = prod_conv(pro, seril.data, 'fir', em)
                return Response({'status': 'success'})
            else:
                print(seril.errors)
                return Response({'status': 'error'})
        else:
            newprod = check
            pd = request.data['products']
            # print(pd)
            # if pd in newprod:
            #     print('hooo')
            products = prod_conv(request.data['products'], newprod, 'sec', em)
            newdata = {
                'delivery_status': 'Undelivered'
            }

            # print(products)
            seril = Soldserializer(check, data=newdata)
            if seril.is_valid():
                seril.save()
                # return Response({'status':seril.data})
                return Response({'status': 'success'})
            else:
                print(seril.errors)
                return Response({'status': 'error'})
            return Response({'status': 'already added'})
    elif request.method == "GET":
        seril = Soldproduct.objects.filter(delivery_status='Undelivered').all()
        result = Soldserializer(seril, many=True)
        return Response({'data': result.data})
    elif request.method == "PUT":

        for i in range(len(request.data)):
            check = Soldproduct.objects.get(id=request.data[i]['id'])
            usr = check.user_id.id
            delv_prod(usr)
            print(usr, 'hi')
            check = Soldproduct.objects.get(id=request.data[i]['id'])
            data = {
                'delivery_status': request.data[i]['delivery_status']
            }
            seril = Soldnewserializer(check, data=data)
            if seril.is_valid():
                seril.save()

            else:
                print(seril.errors)
                return Response({'status': 'error'})
        return Response({'status': 'success'})


@api_view(["GET"])
@permission_classes([permissions.AllowAny, ])
def filtsold(request):
    del_type = request.META['HTTP_DELTYPE']
    del_status = request.META["HTTP_DELSTATUS"]
    city = request.META['HTTP_CITY']
    dat = request.META["HTTP_DAT"]
    data = None
    print(del_type, del_status, city, dat)
    if del_type != "Default" and del_status != "Default" and city != "Default" and dat != "Default":
        data = Soldproduct.objects.filter(
            delivery_type=del_type, delivery_status=del_status, odered_date=dat, user_id__city__contains=city)
    elif del_type != "Default" and del_status != "Default" and city != "Default":
        data = Soldproduct.objects.filter(
            delivery_type=del_type, delivery_status=del_status, user_id__city__contains=city)
    elif del_type != "Default" and del_status != "Default" and dat != "Default":
        data = Soldproduct.objects.filter(
            delivery_type=del_type, delivery_status=del_status, odered_date=dat)
    elif del_type != "Default" and city != "Default" and dat != "Default":
        data = Soldproduct.objects.filter(
            delivery_type=del_type, odered_date=dat, user_id__city__contains=city)
    elif del_status != "Default" and city != "Default" and dat != "Default":
        data = Soldproduct.objects.filter(
            delivery_status=del_status, odered_date=dat, user_id__city__contains=city)
    elif del_type != "Default" and del_status != "Default":
        data = Soldproduct.objects.filter(
            delivery_type=del_type, delivery_status=del_status)
    elif del_type != "Default" and city != "Default":
        data = Soldproduct.objects.filter(
            delivery_type=del_type, user_id__city__contains=city)
    elif del_type != "Default" and dat != "Default":
        data = Soldproduct.objects.filter(
            delivery_type=del_type, odered_date=dat)
    elif del_status != "Default" and city != "Default":
        data = Soldproduct.objects.filter(
            delivery_status=del_status, user_id__city__contains=city)
    elif del_status != "Default" and dat != "Default":
        data = Soldproduct.objects.filter(
            delivery_status=del_status, odered_date=dat)
    elif city != "Default" and dat != "Default":
        data = Soldproduct.objects.filter(
            odered_date=dat, user_id__city__contains=city)
    elif del_type != "Default":
        data = Soldproduct.objects.filter(delivery_type=del_type)
    elif del_status != "Default":
        data = Soldproduct.objects.filter(delivery_status=del_status)
    elif city != "Default":
        data = Soldproduct.objects.filter(user_id__city__contains=city)
    elif dat != "Default":
        data = Soldproduct.objects.filter(odered_date=dat)
    else:
        data = Soldproduct.objects.all()
    result = Soldserializer(data, many=True)

    return Response({'data': result.data})


@api_view(['POST', "GET"])
@permission_classes([permissions.AllowAny, ])
def proddisc(request):
    if request.method == "GET":
        ids = request.META['HTTP_IDS']
        seril = Product.objects.filter(id=ids)
        result = Productserial(seril, many=True)
        return Response({'data': result.data})


@api_view(['POST', "GET", "PUT"])
def addreview(request):
    if request.method == "POST":
        user = request.user.id
        usr = Uerdet.objects.get(userid=user).id
        data = {
            'review': request.data['review'], 'review_reply': '', 'ratings': request.data['ratings'], 'user_id': usr, 'product_id': request.data['product_id']
        }

        check = None
        try:
            check = Reviews.objects.get(
                product_id=request.data['product_id'], user_id=usr, review=request.data['review'])
        except:
            pass
        print(data, check)
        if check == None:
            seril = Reviewserializer(data=data)
            if seril.is_valid():
                seril.save()
                return Response({'status': 'sucess'})
            else:
                print(seril.errors)
                return Response({'status': 'error'})
        else:
            return Response({'status': 'already added'})

    if request.method == "GET":
        ids = request.META['HTTP_IDS']
        seril = Reviews.objects.filter(product_id=ids).all()
        result = SendreviewSeril(seril, many=True)
        return Response({'data': result.data})
    if request.method == "PUT":
        ids = request.META['HTTP_IDS']
        check = None
        try:
            check = Reviews.objects.get(id=ids)
        except:
            pass
        print(check)
        if check != None:
            seril = Reviewserializer(check, data=request.data)
            if seril.is_valid():
                seril.save()
                return Response({'status': 'sucess'})
            else:
                print(seril.errors)
                return Response({'status': 'error'})


@api_view(["POST", "GET", 'DELETE', 'PUT'])
def addtocart(request):
    if request.method == "POST":
        print(request.data)
        user = request.user.id
        usr = Uerdet.objects.get(userid=user)
        print(request.data)
        check = None
        try:
            check = Cart.objects.get(
                user_id=usr.id, product_id=request.data['product_id'], status='Cart')
        except:
            pass
        data = {
            'quantity': request.data['quantity'], 'status': request.data['status'], 'size': request.data['size'], 'user_id': usr.id, 'product_id': request.data['product_id']
        }
        if check == None:
            seril = Cartseril(data=data)
            if seril.is_valid():
                seril.save()
                return Response({'status': 'alert', 'text': 'Product has been added to your cart Thank You!!'})
            else:
                print(seril.errors)
                return Response({'status': 'error', 'text': 'Sorry could not add to the cart!!'})
        else:
            return Response({'status': 'error', 'text': 'Product is already in the cart'})
    elif request.method == "GET":
        status = request.META['HTTP_STATUS']
        print(status)
        seril = None
        if status == 'admin':
            id = request.META['HTTP_ID']
            print(id)
            seril = Cart.objects.filter(solid=id, status='Ondelivery').all()
        else:

            user = request.user.id
            usr = Uerdet.objects.get(userid=user).id

            if status == 'cart':
                seril = Cart.objects.filter(user_id=usr, status='Cart').all()
            elif status == 'delivery':
                seril = Cart.objects.filter(Q(user_id=usr, status='Ondelivery') | Q(
                    user_id=usr, status='Shipped') | Q(user_id=usr, status='Delivered')).all()
            elif status == 'ship':
                seril = Cart.objects.filter(user_id=usr).exclude(status='Sold').exclude(
                    status='Delivery').exclude(status='Cart').all()

        result = Cartgetseril(seril, many=True)
        return Response({'data': result.data})
    elif request.method == 'PUT':
        header = 'Product Shipped'
        disc = 'Your Product has been Shipped from the warehouse. You can track your order on our website.Thank you for shooping'
        em = None
        stat = request.META['HTTP_ID']
        if stat == "Ship":
            search = request.META['HTTP_SEARCH']
            filter = request.META['HTTP_FILTER']
            username = request.META['HTTP_USERNAME']

            check = Cart.objects.filter(solid=search).all()
            for i in range(len(check)):
                data = {
                    'status': filter
                }

                seril = Cartseril(check[i], data=data)
                if seril.is_valid():
                    seril.save()

                    #

                else:
                    print(seril.errors)
            if filter == 'Shipped':
                email_sender(username, header, disc)
        else:
            for i in range(len(request.data)):
                check = Cart.objects.get(id=request.data[i]['id'])
                print('houi', check)
                data = None
                if stat == 'Delivery':
                    data = {
                        'quantity': request.data[i]['quantity'], 'status': 'Delivery',
                    }
                else:
                    data = {
                        'quantity': request.data[i]['quantity'], 'status': request.data[i]['status'],
                    }

                seril = Cartseril(check, data=data)
                if seril.is_valid():
                    seril.save()

                else:
                    print(seril.errors)
                    return Response({'status': 'error'})
        return Response({'status': 'success'})

    elif request.method == 'DELETE':
        print(request.META['HTTP_ID'])
        check = Cart.objects.get(id=request.META['HTTP_ID'])
        print(request.META['HTTP_ID'])
        check.delete()
        return Response({'status': 'success'})


@api_view(['GET'])
@permission_classes([permissions.AllowAny, ])
def usercart(request):

    usr = request.META['HTTP_ID']
    seril = Cart.objects.filter(user_id=usr, status='Delivery').all()

    result = Cartgetseril(seril, many=True)
    return Response({'data': result.data})
