from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from Advertiser.models import Profile, Advertiser, Rating, Favorite
from django.contrib import auth
import re
from django.core.files.storage import default_storage
# Create your views here.

def profile(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, username=request.user.username)
        profile=Profile.objects.get(user=user)
        rate= Rating.objects.filter(user= user).count()
        favorite =  Favorite.objects.filter(user= user).count()
        context={
                'user':user,
                'profile':profile,
                'rate':rate,
                'favorite':favorite,
            }
        if request.method == "POST" and 'update' in request.POST:
            if user.username is not None and user.id != None:
                profile=Profile.objects.get(user=user.id)
                if request.POST['fname'] and request.POST['lname'] and request.POST['username'] and request.POST['email'] and request.POST['password'] and request.POST['bio']:
                    user.first_name=request.POST['fname']
                    user.last_name=request.POST['lname']
                    profile.bio=request.POST['bio']
                    profile.profile_image = request.FILES.get('image')

                    if not request.POST['password'].startswith('pbkdf2_sha256$'):
                        user.set_password(request.POST['password'])                 
                    
                    user.save()
                    profile.save()
                    messages.success(request, 'تم حفظ البيانات')
                    auth.login(request, user)
                                                        
                else:
                    messages.error(request, 'no data')

                return redirect('profile:profile')
            
        return render(request, 'profile_app\profile.html',context)
    else:
        return redirect('profile:profile')

       
def ad_profile(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, username=request.user.username)
        advertiser=Advertiser.objects.get(user_ID=user)
        profile=Profile.objects.get(user=user)
        rate= Rating.objects.filter(user= user).count()
        favorite =  Favorite.objects.filter(user= user).count()
        context={
                'user':user,
                'profile':profile,
                'rate':rate,
                'favorite':favorite,
                'advertiser':advertiser,
            }
        if request.method == "POST" and 'update' in request.POST:
            if user.username is not None and user.id != None:
                profile=Profile.objects.get(user=user.id)
                if request.POST['fname'] and request.POST['lname'] and request.POST['username'] and request.POST['email'] and request.POST['password'] and request.POST['bio']:
                    user.first_name=request.POST['fname']
                    user.last_name=request.POST['lname']
                    profile.bio=request.POST['bio']
                    #profile.profile_image = request.FILES('image')
                    advertiser.ID_number= request.POST['idnumber']
                    advertiser.phone_num=request.POST['phonnum']

                    if not request.POST['password'].startswith('pbkdf2_sha256$'):
                        user.set_password(request.POST['password'])                 
                    
                    if request.FILES.get('profile_image'):
                        profile.is_advertiser=True
                        new_image = request.FILES['profile_image']
                        if profile.profile_image:
                            if default_storage.exists(profile.profile_image.name):
                                default_storage.delete(profile.profile_image.name)
                        profile.profile_image = new_image                     

                    user.save()
                    profile.save()
                    advertiser.save()
                    messages.success(request, 'تم حفظ البيانات')
                    auth.login(request, user)
                                                        
                else:
                    messages.error(request, 'no data')

                return redirect('profile:ad_profile')
            
        return render(request, 'profile_app/ad_profile.html',context)
    else:
        return redirect('profile:profile')
       