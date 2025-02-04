from django.db import models
from datetime import datetime
from django.db.models import Avg
from django.contrib.auth.models import User
# from creditcards.models import CardNumberField,CardExpiryField,SecurityCodeField

    
class AdsSource(models.Model):
    ID = models.AutoField(primary_key=True)
    source_name = models.CharField(max_length=30)
    def __str__(self):
        return self.source_name
    class Meta:
        db_table ='AdsSource'
      
class Services_details(models.Model):     
     ID = models.AutoField(primary_key=True)
     name =models.CharField(max_length=20)
     details = models.TextField( blank=True, null=True)
     class Meta:
        db_table = 'Services_details'
     def __str__(self):
        return self.name
     
class Advertiser(models.Model):
    user_ID = models.OneToOneField(User, on_delete=models.CASCADE)
    ID = models.AutoField(primary_key=True)
    phone_num = models.CharField(max_length=13)
    status = models.BooleanField(default=False)
    ID_number = models.IntegerField()
    def __str__(self):
        return f"Advertiser ID: {self.ID}"
    class Meta:
        db_table ='advertiser'


class Area(models.Model):
    ID = models.AutoField(primary_key=True)
    directorate_name = models.CharField(max_length=30)
    def __str__(self):
        return self.directorate_name
    class Meta:
        db_table ='area'
    def __str__(self):
        return self.directorate_name 

class RealEstateType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20)
    def __str__(self):
        return self.type
    class Meta:
        db_table ='RealEstateType'
    def advertisement_count(self):# this def for count (new for model)
        return Advertisement.objects.filter(RealEstate_id__type_id=self).count()  
    
class RealEstate(models.Model):
    ID = models.AutoField(primary_key=True)
    type_id = models.ForeignKey(RealEstateType , on_delete= models.RESTRICT)
    space = models.DecimalField(decimal_places=3, max_digits=10)
    price = models.DecimalField(decimal_places=2, max_digits= 10)
    attitude= models.DecimalField(decimal_places=6 , max_digits=12, blank=True, null=True)
    longitude= models.DecimalField(decimal_places=6 , max_digits=12,  blank=True, null=True)
    rooms = models.IntegerField(blank=True, null=True)
    floor = models.IntegerField(blank=True, null=True)
    rent_or_sell = models.IntegerField(blank=True, null=True, choices=[(1, 'Rent'), (2, 'Sell')]) 
    class Meta:
        db_table = 'RealEstate'
    def __str__(self):
        return f"{self.type_id} في "
    
class Service(models.Model):
    ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    Services_details_id =models.ForeignKey(Services_details , on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'Service'
    def __str__(self):
        return self.name
    
class Feature(models.Model):
    ID = models.AutoField(primary_key=True)
    feature_name = models.CharField(max_length=40)
    serial_group = models.IntegerField(default=0)
    
    def __str__(self):
        return self.feature_name
    class Meta:
        db_table = 'Feature'
    
class  RealEstate_Feature(models.Model):
    realEstate_ID = models.ForeignKey(RealEstate , on_delete= models.CASCADE)
    feature_ID = models.ForeignKey(Feature, on_delete= models.RESTRICT)
    class Meta:
        db_table = ' RealEstate_Feature'

class Advertisement(models.Model):
    ID = models.AutoField(primary_key=True)
    source = models.ForeignKey(AdsSource , on_delete=models.CASCADE)
    advertiser_id = models.ForeignKey(Advertiser, on_delete= models.CASCADE)
    RealEstate_id = models.ForeignKey(RealEstate, on_delete= models.DO_NOTHING, null= True,  blank=True)
    Service_id = models.ForeignKey(Service , on_delete= models.DO_NOTHING, null= True, blank=True)
    publish_date = models.DateField (default= datetime.now)
    is_active = models.BooleanField(default= True)
    details = models.TextField(null=True, blank=True)
    promoted = models.BooleanField(default=False)
    upddate_date = models.DateField (null= True, blank=True)
    area_id = models.ForeignKey(Area , on_delete = models.RESTRICT)
    status = models.IntegerField(blank=True, choices=[(1, 'قيد الانتظار'), (2, 'قيد المراجعة'), (3, 'منشورة'), (4, 'مرفوضة'), (5, 'محذوفة')], default=1)


    class Meta:
        db_table = 'Advertisement'# يتم تسميه بهذا الاسم في القاعدة
        ordering =['-publish_date']#علشان الترتيب يكون تصاعدي(new)

    def __str__(self):
        return f"Advertisement ID: {self.ID}"
    def average_rating(self):
        # Calculate the average rating for this advertisement
        average = Rating.objects.filter(dvertisement=self).aggregate(Avg('stars'))['stars__avg']
        return average if average is not None else 0  # Return 0 if no ratings exist(new)
    
class RealEstateImage(models.Model):
    RealEstate_id = models.ForeignKey(
        RealEstate, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', null=True)
    class Meta:
        db_table = 'RealEstateImage'



class Rating(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # 1 to 5 stars
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('advertisement', 'user')  # Ensure a user can only rate an ad once

    def __str__(self):
        return f"{self.user} rated {self.advertisement} with {self.stars} stars"
# Create your models here.
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'advertisement')  # Ensure no duplicate favorites per user
        db_table = 'Favorite'

    def __str__(self):
        return f"{self.user.username} favorited {self.advertisement}"
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(blank=True, default=':)', max_length=355)
    profile_image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_advertiser=models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username
    class Meta:
        db_table = 'Profile'    
 



