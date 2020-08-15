
from django.urls import path, include
from rest_framework import routers
from.views import signup_user, user_details, reset_password, user_single_details


router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('signup/', signup_user),



]
