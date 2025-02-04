from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from Advertiser.models import AdsSource,Services_details,Advertiser,Area,RealEstateType,RealEstate,Service,Feature,RealEstate_Feature,Advertisement,RealEstateImage,Rating

class Aboutus(models.Model):
    ID = models.AutoField(primary_key=True)
    details = models.TextField( blank=True, null=True)
    class Meta:
        db_table = 'Aboutus'


        