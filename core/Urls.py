from django.urls import path
from . import views

urlpatterns=[
    path ('',views.index,name='index'),
    path ('see_ads',views.see_ads,name='see_ads'),
     path ('search',views.search,name='search'),
    path ('<int:ads_id>',views.see_ads_details,name='see_ads_details'),
    path ('see_servecs',views.see_servecs,name='see_servecs'),
    path ('favorate',views.favorate,name='favorate'),
    path('toggle_favorite/<int:ad_id>/', views.toggle_favorite, name='toggle_favorite'),

]