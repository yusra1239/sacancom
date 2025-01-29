# Create your forms here.
from .models import Feature , RealEstateType, Area, Advertisement , Advertiser
from .models import Service , Services_details, RealEstate
from .models import RealEstate_Feature, RealEstateImage, Profile
from .models import AdsSource
from django.contrib.auth.models import User  
from django.contrib.auth.forms import UserCreationForm
from django import forms
class NewUserForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-dark text-white',
            'placeholder': 'first name',
        })
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-dark text-white',
            'placeholder': 'last name',
        })
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-dark text-white',
            'placeholder': 'Username',
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-dark text-white',
            'placeholder': 'Email',
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-dark text-white',
            'placeholder': 'Password',
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-dark text-white',
            'placeholder': 'Confirm Password',
        })
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_image']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Bio'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
