from django.urls import path
from . import views
app_name = 'profile_app' 
urlpatterns=[
    path ('profile',views.profile, name='profile'),
    ]