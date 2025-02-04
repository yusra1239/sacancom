from django.urls import path
from . import views

app_name="profile"
urlpatterns=[
    path ('profile',views.profile, name='profile'),
    path ('ad_profile',views.ad_profile, name='ad_profile'),
    ]