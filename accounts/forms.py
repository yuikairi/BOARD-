from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from django.contrib.auth.forms import UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=100)
    profile_picture = forms.ImageField(label='本人確認書類', required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'profile_picture')
        

class UserEditForm(forms.ModelForm):
    profile_picture = forms.ImageField(label='本人確認写真',required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email','profile_picture')

class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(max_length=100)
    profile_picture = forms.ImageField(label='本人確認写真', required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'profile_picture')
        
