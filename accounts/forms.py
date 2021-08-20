from django import forms
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory

from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        verbose_name = 'Formulário De UserProfile'
        exclude = ['user', 'picture','creator']

class UserProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        verbose_name = 'Formulário De UserProfile'
        exclude = ['user','occupation','profile','creator']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        verbose_name = 'Formulário De User'
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

UserFormset = inlineformset_factory(User, UserProfile, extra=0, can_delete=False, exclude=['creator','picture'], min_num=1)

class PasswordChangeForm(forms.ModelForm):
    class Meta:
        model = User
        verbose_name= 'Formulário alteração de senha de usuário'
        fields = ['username', 'password']