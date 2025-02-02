from django.urls import path
from . import views

app_name="account"
urlpatterns = [

    path('adsSignup', views.adsSignup, name='adsSignup'),
    path('usersignup', views.usersignup, name='usersignup'),
    path('adslogin', views.adslogin, name='adslogin'),
    path('profile <str:username>', views.profile, name='profile'),
    path('vistorlogin', views.vistorlogin, name='vistorlogin'),
    path('logout', views.logout, name='logout'),
    path('payment', views.payment , name='payment'),
    path("save_card/",views.save_card, name="save_card"),
]