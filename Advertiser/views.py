from django.shortcuts import get_object_or_404, render , redirect
# Create your views here.
from django.contrib import messages
from django.http import Http404
from .models import Feature , RealEstateType, Area, Advertisement , Advertiser
from .models import Service , Services_details, RealEstate
from .models import RealEstate_Feature, RealEstateImage
from .models import AdsSource
from django.contrib.auth.models import User
from django.contrib import auth
from datetime import date



def dashbord(request):
    is_auth= False
    ad_id=None
    data=None
    
    if request.user.is_authenticated:
        user = request.user 
        try:
            ad_id= get_object_or_404( Advertiser,user_ID=user.id)
            if ad_id is not None:
                is_auth=True
                data=Advertisement.objects.filter(advertiser_id__ID = ad_id.ID)
            else:
                is_auth=False
        except Http404:
            is_auth=False
    else:
        is_auth=False

    context={
            'user':ad_id,
            'ads_data':data,
            'is_auth':is_auth,
            }
    
    return render(request,"advertiser/dashbord.html", context)

def form_ads(request):
    if request.user.is_authenticated:
        user = request.user
        ad_id = Advertiser.objects.get(user_ID = user.id)
       
        feature = []
        type_id = None
        rooms = None
        floor = None
        status = None
        promote = None
        r_or_s = None
        space = None
        price = None
        address = None
        details = None
        user = None
        source = AdsSource.objects.get(ID=1)

        if request.method == 'POST' and 'save' in request.POST:
            user = request.POST.get('user')
            feature = request.POST.getlist('features')
            type_id = request.POST.get('realEstate_type')
            status = request.POST.get('status')
            promote = request.POST.get('promote')
            r_or_s = request.POST.get('rent_or_sell')
            space = request.POST.get('space')
            price = request.POST.get('price')
            address = request.POST.get('address')
            img_files = request.FILES.getlist('image')  # Get the list of uploaded files
            details = request.POST.get('details')

            # Collect errors
            errors = []

            if not user:
                errors.append('يرجى اختيار المستخدم.')
            if not type_id:
                errors.append('يرجى اختيار نوع العقار.')
            if not status:
                errors.append('يرجى اختيار حالة الإعلان.')
            if not promote:
                errors.append('يرجى اختيار خيار الترويج.')
            if not r_or_s:
                errors.append('يرجى اختيار خيار البيع أو الإيجار.')
            if not space:
                errors.append('يرجى إدخال مساحة العقار.')
            if not price:
                errors.append('يرجى إدخال السعر.')
            if not address:
                errors.append('يرجى اختيار العنوان.')
            if not img_files:
                errors.append('يرجى تحميل صورة واحدة على الأقل.')

            if errors:
                for error in errors:
                    messages.error(request, error)
            else:
                try:
                    user_obj = Advertiser.objects.get(ID=user)
                    type_obj = RealEstateType.objects.get(id=type_id)
                    address_obj = Area.objects.get(ID=address)
                    # Create RealEstate instance

                    realestate = RealEstate(
                        type_id=type_obj,   
                        longitude=request.POST['longitude'],  
                        attitude=request.POST['latitude'],  
                        space=space,
                        price=price,
                        rooms=rooms,
                        floor=floor,
                        rent_or_sell=r_or_s
                    )
                    realestate.save()

                    # Create Advertisement instance
                    ads = Advertisement(
                        source=source,
                        advertiser_id=user_obj,
                        RealEstate_id=realestate,
                        is_active=status,
                        details=details,
                        promoted=promote,
                        area_id=address_obj,
                    )
                    ads.save()
                    
                    # Save each image
                    for img in img_files:
                        realEstateImage = RealEstateImage(RealEstate_id=realestate, photo=img)
                        realEstateImage.save()
                

                    for feature_id in feature:
                        fe=Feature.objects.get(ID=feature_id)
                        f=RealEstate_Feature( feature_ID = fe , realEstate_ID= realestate)
                        f.save()

                    messages.success(request, 'تم اضافة الاعلان بنجاح')
                except Exception as e:
                    messages.error(request, f'خطأ: {str(e)}')

    context = {
            'user':ad_id,
            'features': Feature.objects.filter(serial_group=0),
            'Feature_gro': Feature.objects.filter(serial_group__gt=0).order_by('serial_group'),
            'r_type': RealEstateType.objects.all(),
            'area': Area.objects.all(),
            'try':feature,
        }
    return render(request, "advertiser/form_ads.html", context)

def form_ads2(request):
    if request.user.is_authenticated:
        u = request.user
        ad_id = Advertiser.objects.get(user_ID = u.id)

        context ={
            'service_de':Services_details.objects.all(),
            'area': Area.objects.all(),
            'user':ad_id,
                    }
        
        service_id= None
        status=None
        address_id=None
        details=None
        user=None
        source_obj= AdsSource.objects.get(ID=2)
        is_added= None
        
        
        if  request.method == 'POST' and 'save' in request.POST:
            
            if 'user' in request.POST:
                user = request.POST['user']
            else:messages.error(request, 'error in user')

            if 'service' in request.POST:
                service_id = request.POST['service']
            else:
                messages.error(request,'خطأ في الخدمات')
            
            if 'address' in request.POST:
                address_id = request.POST['address']
            else:
                messages.error(request, 'خطأ في العنوان')

            if 'status' in request.POST:
                status= request.POST['status']
            else:
                messages.error(request, 'خطأ في حالة الاعلان')

            if 'details' in request.POST:
                details= request.POST['details']

            if user and service_id and address_id and status:           
                try:
                    user_obj = Advertiser.objects.get(ID=user)
                except Advertiser.DoesNotExist:
                        messages.error(request,'ERROR in user !!')
                        user_obj = None
                try:
                    service_obj = Services_details.objects.get(ID=service_id)
                except Services_details.DoesNotExist:
                        messages.error(request,'خطأ في الخدمات')
                        service_obj = None
                try:
                    address_obj = Area.objects.get(ID = address_id)
                except Area.DoesNotExist:
                        messages.error(request,'خطأ في العنوان')
                        address_obj = None

            
                serv= Service(name=service_obj,
                            Services_details_id= service_obj)
                serv.save()
                ads= Advertisement(source= source_obj, advertiser_id= user_obj, 
                            Service_id=serv,is_active= status, area_id =address_obj,
                            details= details)
                ads.save()
                messages.success(request , 'تم اضافة الاعلان بنجاح')
                return redirect('advertiser_app:dashbord')
            
            else:
                messages.error(request, 'تأكد من الحقول الفارغة')
                return render(request, 'advertiser/form_ads2.html',{
                    'service_de':Services_details.objects.all(),
                    'area': Area.objects.all(),
                    'user':Advertiser.objects.filter(ID= 1),
                    'service_id':service_id,
                    'address_id':address_id,
                    'details':details,
                    'status':status,

                })

        return render(request, "advertiser/form_ads2.html", context)

def update_form_ads(request, ad_id):
   
    if request.user.is_authenticated:
        u = request.user
        feature_obj=[]
        source = AdsSource.objects.get(ID=1)

        try:
            advertiser= get_object_or_404( Advertiser,user_ID=u.id)
            ad= Advertisement.objects.get(ID = ad_id)
            ad_realestate=RealEstate.objects.get(ID= ad.RealEstate_id.ID)
            re_feature = RealEstate_Feature.objects.filter(realEstate_ID = ad_realestate.ID )

           
            if advertiser is not None:
                is_auth=True
            else:
                is_auth=False

            for f in re_feature:
                if f.realEstate_ID.ID == ad.RealEstate_id.ID and f.realEstate_ID not in feature_obj:
                    feature_obj.append(f.feature_ID.ID)

            context = {
            'user': advertiser,
            'features': Feature.objects.filter(serial_group=0),
            'Feature_gro': Feature.objects.filter(serial_group__gt=0).order_by('serial_group'),
            'r_type': RealEstateType.objects.all(),
            'area': Area.objects.all(),
            'ad_feature':feature_obj,
            'ad_realestate':ad_realestate,
            'ad_realestate_img':RealEstateImage.objects.filter(RealEstate_id=ad.RealEstate_id),
            'ad_data':ad,
            'is_auth':is_auth
            }
        
            if request.method == 'POST' and 'update' in request.POST:
                user = request.POST.get('user')
                feature = request.POST.getlist('faetures')
                type_id = request.POST.get('realEstate_type')
                rooms = request.POST.get('rooms')
                floor = request.POST.get('floor')
                status = request.POST.get('status')
                promote = request.POST.get('promote')
                r_or_s = request.POST.get('rent_or_sell')
                space = request.POST.get('space')
                price = request.POST.get('price')
                address = request.POST.get('address')
                latitude= request.POST.get('latitude')
                longitude= request.POST.get('longitude')
                # img_files = request.FILES.getlist('image')  # Get the list of uploaded files
                details = request.POST.get('details')

                # Collect errors
                errors = []

                if not user:
                    errors.append('يرجى اختيار المستخدم.')
                if not type_id:
                    errors.append('يرجى اختيار نوع العقار.')
                if not rooms:
                    errors.append('يرجى إدخال عدد الغرف.')
                if not status:
                    errors.append('يرجى اختيار حالة الإعلان.')
                if not promote:
                    errors.append('يرجى اختيار خيار الترويج.')
                if not r_or_s:
                    errors.append('يرجى اختيار خيار البيع أو الإيجار.')
                if not space:
                    errors.append('يرجى إدخال مساحة العقار.')
                if not price:
                    errors.append('يرجى إدخال السعر.')
                if not address:
                    errors.append('يرجى اختيار العنوان.')
                if not longitude:
                    errors.append('يرجى التأكد الموقع الجغرافي.')
                if not latitude:
                    errors.append('يرجى التأكد الموقع الجغرافي.')
            # if not img_files:
            #     errors.append('يرجى تحميل صورة واحدة على الأقل.')

                if errors:
                    for error in errors:
                        messages.error(request, error)
                else:
                    try:
                        user_obj = Advertiser.objects.get(ID=user)
                        type_obj = RealEstateType.objects.get(id=type_id)
                        address_obj = Area.objects.get(ID=address)

                        # Create RealEstate instance
                        ad_realestate.type_id=type_obj
                        
                        ad_realestate.longitude= longitude
                        ad_realestate.attitude=latitude  
                        ad_realestate.space=space
                        ad_realestate.price=price
                        ad_realestate.rooms=rooms
                        ad_realestate.floor=floor
                        ad_realestate.rent_or_sell=r_or_s
                        
                        ad_realestate.save()

                        # Create Advertisement instance
                        
                        ad.source=source
                        ad.advertiser_id=user_obj
                        ad.RealEstate_id=ad_realestate
                        ad.is_active=status
                        ad.details=details
                        ad.promoted=promote
                        ad.area_id=address_obj
                        ad.upddate_date= date.today()
                        
                        ad.save()

                        # Save each image
                        # for img in img_files:
                        #     realEstateImage = RealEstateImage(RealEstate_id=realestate, photo=img)
                        #     realEstateImage.save()

                        update_re_feature(realestate_id=ad_realestate, new_feature=feature)
                        messages.success(request,'تم التعديل بنجاح')
                        return redirect('advertiser_app:dashbord')

                    except Exception as e:
                        messages.error(request, f'خطأ: {str(e)}')

            return render(request, "advertiser/update_form_ads.html", context)
        except Http404:
                is_auth=False

def update_form_ads2(request, ad_id):
    if request.user.is_authenticated:
        u = request.user
        try:
            advertiser= get_object_or_404( Advertiser,user_ID=u.id)
            ad= Advertisement.objects.get(ID = ad_id)
            ad_servise= Service.objects.get(ID = ad.Service_id.ID)
            if ad_id is not None:
                is_auth=True
            else:
                is_auth=False

            context ={
            'service_de':Services_details.objects.all(),
            'area': Area.objects.all(),
            'user':advertiser,
            'ad_servise':ad_servise,
            'ad':ad,
            'is_auth':is_auth,
                }

            if request.method == 'POST' and 'update' in request.POST:

                if 'user' in request.POST:
                        user = request.POST['user']
                else:
                    messages.error(request, 'error in user')

                if 'service' in request.POST:
                    service_id = request.POST['service']
                else:
                    messages.error(request, 'خطأ في الخدمات')

                if 'address' in request.POST:
                    address_id = request.POST['address']
                else:
                    messages.error(request, 'خطأ في العنوان')

                if 'status' in request.POST:
                    status = request.POST['status']
                else:
                    messages.error(request, 'خطأ في حالة الاعلان')

                if 'details' in request.POST:
                    details = request.POST['details']

                if user and service_id and address_id and status:

                    try:
                        user_obj = Advertiser.objects.get(ID=advertiser.ID)
                    except Advertiser.DoesNotExist:
                        messages.error(request, 'خطأ في المستخدم')
                        user_obj = None
                    try:
                        service_obj = Services_details.objects.get(ID=service_id)
                    except Services_details.DoesNotExist:
                        messages.error(request, 'خطأ في الخدمة')
                        service_obj = None
                    try:
                        address_obj = Area.objects.get(ID=address_id)
                    except Area.DoesNotExist:
                        messages.error(request, 'خطأ في العنوان')
                        address_obj = None
                
                    ad_servise.name = service_obj.name
                    ad_servise.Services_details_id = service_obj
                    ad_servise.save()

                    ad.source = AdsSource.objects.get(ID=2)
                    ad.advertiser_id = user_obj
                    ad.Service_id = ad_servise
                    ad.is_active = status
                    ad.details = details
                    ad.area_id=address_obj
                    ad.upddate_date= date.today()

                    ad.save()
                    messages.success(request, 'تم تعديل بيانات الاعلان بنجاح')
                    return redirect("advertiser_app:dashbord")
                else:
                    messages.error(request, 'لم يتم تعديل البيانات')
                    return redirect("advertiser_app:dashbord")
        except Http404:
            is_auth=False

    else:
        return render(request,"advertiser/update_form_ads2.html", context ,  messages.error(request, 'no permissions'))    
    return render(request,"advertiser/update_form_ads2.html", context)    

def update_re_feature(realestate_id, new_feature):
    RealEstate_Feature.objects.filter(realEstate_ID = realestate_id ).delete()
    for feature_id in new_feature:
        fe=Feature.objects.get(ID=feature_id)
        f=RealEstate_Feature( feature_ID = fe , realEstate_ID=realestate_id )
        f.save()
    pass