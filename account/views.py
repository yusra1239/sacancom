from django.shortcuts import get_object_or_404, render , redirect
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib import messages
from Advertiser.models import Advertiser, AdsSource
from django.contrib.auth.models import User
import re
from django.contrib import auth
#from advertiser_app.models import Feature , RealEstateType, Area, advertisement , User , Advertiser

def adsSignup(request):
    
    username = None
    email = None
    f_name= None
    l_name= None
    password= None
    conf_password= None
    is_added=None
    id_number=None

    if request.method == 'POST' and 'adssignup' in request.POST:
       
       ## Get values
        if 'username' in request.POST: 
          username= request.POST['username']
        else:
            messages.error(request, 'خطأ في اسم المستخدم')
       
        if 'fname' in request.POST: 
           f_name= request.POST['fname']
        else:
            messages.error(request, 'خطأ في الاسم الاول')
       
        if 'lname' in request.POST: 
           l_name= request.POST['lname']
        else:
            messages.error(request, 'خطأ في الاسم الاخير')
      
        if 'email' in request.POST: 
           email= request.POST['email']
        else:
            messages.error(request, 'خطأ في البريد الالكتروني')
       
        if 'pass' in request.POST: 
           password = request.POST['pass']
        else:
            messages.error(request, 'خطأ في كلمة المرور')
       
        if 'conf_pass' in request.POST: 
           conf_password= request.POST['conf_pass']
        else:
            messages.error(request, 'خطأ في كلمة المرور')
        
        if 'phone_num' in request.POST: 
           phone_num= request.POST['phone_num']
        else:
            messages.error(request, 'خطأ في رقم الهاتف')
        
        if 'idnumber' in request.POST: 
           id_number= request.POST['idnumber']
        else:
            messages.error(request, 'خطأ في الرقم الوطني')

        if username and f_name and l_name and email and password and conf_password and phone_num and id_number:
            if password == conf_password:
                if (Advertiser.objects.filter(ID_number= id_number)).exists():
                    messages.error(request, ' تأكد من الرقم الوطني.!')
                else:
                    if( User.objects.filter(username= username)).exists():
                        messages.error(request, ' اسم المستخدم موجود مسبقا .!')
                    else:
                        if User.objects.filter(email=email).exists():
                            messages.error(request, ' البريد الالكتروتي موجود مسبقا .!')
                        else:
                            patt = "^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
                            if re.match(patt, email):
                                # add user
                                user= User.objects.create_user(first_name = f_name, 
                                                               last_name= l_name,
                                                                email=email, 
                                                                username=username, 
                                                                password= password)
                                user.save()
                                ad = Advertiser(user_ID=user, 
                                                phone_num= phone_num, 
                                                status= True, 
                                                ID_number=id_number)
                                ad.save()
                                #clear fields after registed
                                f_name=''
                                l_name=''
                                email=''
                                username=''
                                password=''
                                conf_password=''
                                id_number=''
                                messages.success(request,'تم')
                                return redirect("advertiser_app:dashbord")
                            else:
                                messages.error(request,'البريد الالكتروني غير صالح')
            else:
                messages.error(request, 'تأكد من تطابق حقول كلمة المرور و تأكيد كلمة المرور')

        else:
            messages.error(request, 'تأكد من الحقول الفارغة ')
        # send the data that has been enter if there is error in some fields
        return render(request, "account/usersignup.html", {
            'fname':f_name,
            'lname':l_name,
            'email':email,
            'username':username,
            'pass':password,
            'conf_pass':conf_password,
            'is_added':is_added
        })
    
    else:
        return render(request, "account/AdsSignup.html",)

def usersignup(request): 
    username = None
    email = None
    f_name= None
    l_name= None
    password= None
    conf_password= None
    is_added=None
    if request.method == 'POST' and 'uersignup' in request.POST:
       
       ## Get values
        if 'username' in request.POST: 
          username= request.POST['username']
        else:
            messages.error(request, 'خطأ في اسم المستخدم')
       
        if 'fname' in request.POST: 
           f_name= request.POST['fname']
        else:
            messages.error(request, 'خطأ في الاسم الاول')
       
        if 'lname' in request.POST: 
           l_name= request.POST['lname']
        else:
            messages.error(request, 'خطأ في الاسم الاخير')
      
        if 'email' in request.POST: 
           email= request.POST['email']
        else:
            messages.error(request, 'خطأ في البريد الالكتروني')
       
        if 'pass' in request.POST: 
           password = request.POST['pass']
        else:
            messages.error(request, 'خطأ في كلمة المرور')
       
        if 'conf_pass' in request.POST: 
           conf_password= request.POST['conf_pass']
        else:
            messages.error(request, 'خطأ في كلمة المرور')

        if username and f_name and l_name and email and password and conf_password:
            if password == conf_password:
                if( User.objects.filter(username= username)).exists():
                    messages.error(request, ' اسم المستخدم موجود مسبقا .!')
                else:
                    if User.objects.filter(email=email).exists():
                        messages.error(request, ' البريد الالكتروتي موجود مسبقا .!')
                    else:
                        patt = "^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
                        if re.match(patt, email):
                            # add user
                            user= User.objects.create_user(first_name = f_name, last_name= l_name,
                                                email=email, username=username, password= password)
                            user.save()
                            #clear fields after registed
                            f_name=''
                            l_name=''
                            email=''
                            username=''
                            password=''
                            conf_password=''
                            messages.success(request,'تم')
                            is_added=True

                        else:
                            messages.error(request,'البريد الالكتروني غير صالح')
            else:
                messages.error(request, 'تأكد من تطابق حقول كلمة المرور و تأكيد كلمة المرور')

        else:
            messages.error(request, 'تأكد من الحقول الفارغة ')
        # send the data that has been enter if there is error in some fields
        return render(request, "account/usersignup.html", {
            'fname':f_name,
            'lname':l_name,
            'email':email,
            'username':username,
            'pass':password,
            'conf_pass':conf_password,
            'is_added':is_added
        })
    
    else:
        return render(request, "account/usersignup.html")

def adslogin(request):
    
    username =None
    password =None
    rememberme=None
    adv=None
    
    if request.method == 'POST' and 'adslogin' in request.POST:

        if 'username' in request.POST:username = request.POST['username']
        else:messages.error(request, 'خطأ في اسم المستخدم')

        if 'pass' in request.POST:password = request.POST['pass']
        else:messages.error(request, 'خطأ في كلمة المرور')

        if 'rememberme' in request.POST: rememberme= request.POST['rememberme']

        if username and password:
                user = auth.authenticate(username = username, password= password)
                
                if user is not None:
                    try:
                        adv= get_object_or_404( Advertiser,user_ID=user.id)
                        if adv is not None:
                            auth.login(request, user)
                            return redirect('advertiser_app:dashbord')
                        else:
                            messages.error(request, 'ليس لديك صلاحيات للاعلان ... قم بانشاء حساب اولا')
                    except Http404:
                        messages.error(request,'ليس لديك صلاحيات للاعلان .. قم بانشاء حساب اولا')
                      
                else:         
                    messages.error(request,'خطأ في اسم المستخدم او كلمة المرور')
        else:         
            messages.error(request,'خطأ في اسم المستخدم او كلمة المرور')
    
    return render(request, "account/Adslogin.html",)

def profile(request, username):
    user = get_object_or_404(User, username=username)
    context = {
        'user': user,
    }
    return render(request, 'account/profile.html', context)

def vistorlogin(request):

    username =None
    password =None
    rememberme=None
    
    if request.method == 'POST' and 'login' in request.POST:
        messages.success(request, 'success')
        if 'username' in request.POST:username = request.POST['username']
        else:messages.error(request, 'خطأ في اسم المستخدم')

        if 'pass' in request.POST:password = request.POST['pass']
        else:messages.error(request, 'خطأ في كلمة المرور')

        if 'rememberme' in request.POST: rememberme= request.POST['rememberme']

        if username and password:
            user = auth.authenticate(username = username, password= password)

            if user is not None :
                auth.login(request, user)
                return render(request, 'core/index.html')
            else:
                messages.error(request,'خطأ في اسم المستخدم او كلمة المرور')

    return render(request, "account/vistorlogin.html",)


def logout (request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect("index")

# Create your views here.
