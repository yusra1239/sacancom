from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from Advertiser.models import Profile
from django.contrib import auth
# Create your views here.
def profile(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, username=request.user.username)
        context = {
            'user': user,
        }
    return render(request, 'profile_app\profile.html', context)