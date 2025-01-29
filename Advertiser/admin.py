from django.contrib import admin
from .models import AdsSource 
from .models import Area
from .models import RealEstateType
from .models import Service
from .models import RealEstate
from .models import Advertisement
from .models import Feature
from .models import RealEstate_Feature
from .models import RealEstateImage
from .models import Services_details
from .models import Rules
from .models import Advertiser
from .models import Rating

admin.site.register(AdsSource)
admin.site.register(Area)
admin.site.register(RealEstateType)
admin.site.register(Service)
admin.site.register(RealEstate)
admin.site.register(Advertisement)
admin.site.register(Feature)
admin.site.register(RealEstate_Feature)
admin.site.register(RealEstateImage)
admin.site.register(Services_details)
admin.site.register(Advertiser)
admin.site.register(Rules)
admin.site.register(Rating)

