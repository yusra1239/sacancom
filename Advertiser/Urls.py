from django.urls import path
from . import views

app_name = "advertiser_app"

urlpatterns = [
    path('dashbord/', views.dashbord, name='dashbord'),  # Ensure the view name matches
    path('form_ads', views.form_ads, name='form_ads'),
    path('form_ads2', views.form_ads2, name='form_ads2'),
    path('update_form_ads2/<int:ad_id>', views.update_form_ads2, name='update_form_ads2'),
    path('update_form_ads/<int:ad_id>', views.update_form_ads, name='update_form_ads'),
]