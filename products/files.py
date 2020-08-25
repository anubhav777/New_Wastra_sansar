from django.conf import settings
import os
from .models import Cart
from .serializers import Cartseril
from django.core.mail import send_mail
from django.contrib.auth.models import User


def folder_make(obj):
    pt = settings.BASE_DIR
    new_pt = f"{pt}\media\{obj}"
    if not os.path.exists(new_pt):
        os.mkdir(new_pt)
        return new_pt
    else:
        print('hi')
        return new_pt


all_img = ['JPG', 'PNG', 'JPG']


def allowed_image(file):

    filename = str(file)

    if not "." in filename:

        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in all_img:
        print('done')
        return True
    else:

        return False


def file_checker(filename):
    if not os.path.exists(filename):
        return True
    else:
        return False


def specify(obj):
    dj = None
    if "\n" in obj:
        dj = obj.split("\n")
    elif "," in obj:
        dj = obj.split(",")

    else:
        return obj
    newobj = {}
    for i in range(len(dj)):
        if dj[i] != '':
            newobj.update({str(i): dj[i]})

    print(newobj)
    return newobj


def prod_conv(obj, oldobj, typ, em):
    newobj = {}
    header = 'Product Odered'
    disc = 'Your Product has been odered. You can track your order on our website.Thank you for shooping'

    for i in range(len(obj)):

        if typ == 'fir':
            check = Cart.objects.get(id=obj[i]['id'])
            data = {
                'solid': oldobj['id'],
                'status': 'Ondelivery'
            }
            seril = Cartseril(check, data=data)
            if seril.is_valid():
                seril.save()
                print('heheh')

            else:
                print(seril.errors)
            # check=Cart.objects.get(id=obj[i]['id'])
            # data={
            #     'solid':1
            # }
            # seril=Cartseril(check,data=data)
            # if seril.is_valid():
            #     seril.save()

            # else:
            #     print(seril.errors)
        else:

            check = Cart.objects.get(id=obj[i]['id'])
            data = {
                'solid': oldobj.id,
                'status': 'Ondelivery'
            }
            seril = Cartseril(check, data=data)
            if seril.is_valid():
                seril.save()
                print('heheh')
                adminemail()
                email_sender(em, header, disc)

            else:
                print(seril.errors)
            # if obj[i]['product_id']['id'] in oldobj.values():
            #     print('hohohohoho')
            # else:

            #     l=len(oldobj)
            #     newobj.update({(l+i):obj[i]['product_id']['id']})

    return newobj


def adminemail():
    header = "Product Order Alert"
    disc = "A product has been placed please check the website for more details"
    adm = User.objects.filter(is_superuser=True).all()
    for j in range(len(adm)):

        user = User.objects.get(username=adm[j])
        user_email = user.email
        email_sender(user_email, header, disc)
        print(user_email)


def delv_prod(userid):
    seril = Cart.objects.filter(user_id=userid, status='Delivery').all()
    for i in range(len(seril)):
        data = {
            'status': 'Sold'
        }

        res = Cartseril(seril[i], data=data)
        if res.is_valid():
            res.save()
        else:
            print(res.errors)


def ratavg(obj):
    tot = 0
    cnt = 0
    newavg = 0
    try:
        for i in range(len(obj)):

            tot += obj[i].ratings
            cnt += 1
        newavg = round(tot/cnt)
    except:
        pass
    return newavg
    print(newavg)


def email_sender(newemail, header, dis):
    send_mail(header, f'''{dis}
        
        ''', 'magaranub@gmail.com', [newemail])
