
from django.conf import settings
import jwt
import datetime
from datetime import timedelta
from .models import Uerdet
from .serializers import Userdetailsserializer, Usersecserializer


def token_genrator(email):
    obj = {'email': email, 'exp': datetime.datetime.utcnow() +
           datetime.timedelta(minutes=30)}
    secret = settings.SECRET_KEY
    token = jwt.encode(obj, secret, algorithm='HS256')
    send_em = email_sender(email, token)


def Userextra(obj, data):

    newdata = {
        "address": data['address'],
        "state": data['state'],
        "city": data['city'],
        "phone": data['phone'],
        "userid": obj['id']
    }
    print(obj['id'])
    checker = None
    try:
        checker = Uerdet.objects.get(userid=obj['id'])
    except:
        pass
    if checker == None:
        seril = Usersecserializer(data=newdata)
        if seril.is_valid():
            seril.save()
            return True
        else:
            print(seril.errors)
            return Fasle
    else:
        print('hi')
        seril = Usersecserializer(checker, data=newdata)
        if seril.is_valid():
            seril.save()
            return True
        else:
            print(seril.errors)
            return False
