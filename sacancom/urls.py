
from django.contrib import admin
from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',include('core.Urls')),
    path('sacancom/',include('Advertiser.Urls')),
    path('admin/', admin.site.urls),
    path('sacancom/login/', include('account.urls'), name="account" ),
    path('sacancom/profile/', include('profile_app.urls'), name="profile_app" )

     ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
