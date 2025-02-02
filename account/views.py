from django.shortcuts import get_object_or_404, render , redirect
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib import messages
from Advertiser.models import Advertiser, AdsSource
from django.contrib.auth.models import User
import re
from django.http import HttpResponse
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
                            patt = r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"

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
                        patt = r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"

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

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import CreditCard
import datetime

@login_required
def payment(request):
    ad_id = request.GET.get('ad_id')
    if request.method == "POST":
        phone_num = request.POST.get("phone_num")
        card_number = request.POST.get("card_number").replace(" ", "")
        expiry_date = request.POST.get("expire").split("/")
        security_code = request.POST.get("security_code")

        if len(expiry_date) != 2:
            return HttpResponse("<h3 style='color:red;'>تاريخ الانتهاء غير صالح</h3>")

        expiry_month, expiry_year = map(int, expiry_date)
        expiry_year = int("20" + str(expiry_year)) if len(str(expiry_year)) == 2 else expiry_year

        if expiry_year < datetime.datetime.now().year or (
            expiry_year == datetime.datetime.now().year and expiry_month < datetime.datetime.now().month
        ):
            return HttpResponse("<h3 style='color:red;'>البطاقة منتهية الصلاحية</h3>")

        try:
            card = CreditCard(
                expiry_month=expiry_month,
                expiry_year=expiry_year,
                security_code=security_code
            )
            card.set_card_number(card_number)  # تشفير الرقم قبل الحفظ
            card.full_clean()  # التحقق من صحة البيانات
            card.save()
            return HttpResponse("<h3 style='color:green;'>تمت عملية الدفع بنجاح ✅</h3>")
        except Exception as e:
            return HttpResponse(f"<h3 style='color:red;'>خطأ في الدفع: {e}</h3>")

    return render(request, "account/payment.html",{'ad_id': ad_id})



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CreditCard
def luhn_check(card_number: str) -> bool:
    """التحقق من صحة رقم البطاقة باستخدام خوارزمية Luhn"""
    card_number = card_number.replace(" ", "")
    if not card_number.isdigit():
        return False

    total = 0
    reverse_digits = list(map(int, card_number[::-1]))

    for i, digit in enumerate(reverse_digits):
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit

    return total % 10 == 0
@csrf_exempt
def save_card(request):
    """واجهة API لحفظ بطاقة الائتمان"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            required_fields = ["card_number", "expiry_month", "expiry_year", "security_code", "card_holder_name"]
            if not all(field in data for field in required_fields):
                return JsonResponse({"error": "جميع الحقول مطلوبة!"}, status=400)

            card_number_clean = data["card_number"].replace(" ", "")
            expiry_year_full = int("20" + str(data["expiry_year"])) if len(str(data["expiry_year"])) == 2 else int(data["expiry_year"])

            if not luhn_check(card_number_clean):
                return JsonResponse({"error": "رقم البطاقة غير صالح!"}, status=400)

            if expiry_year_full < datetime.datetime.now().year or (
                expiry_year_full == datetime.datetime.now().year and int(data["expiry_month"]) < datetime.datetime.now().month
            ):
                return JsonResponse({"error": "البطاقة منتهية الصلاحية!"}, status=400)

            card = CreditCard(
                card_number=card_number_clean,
                expiry_month=int(data["expiry_month"]),
                expiry_year=expiry_year_full,
                security_code=data["security_code"],
                card_holder_name=data["card_holder_name"]
            )
            card.full_clean()
            card.save()

            return JsonResponse({"message": "تم حفظ البطاقة بنجاح!"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "تنسيق JSON غير صحيح!"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "يجب إرسال البيانات عبر POST"}, status=405)
