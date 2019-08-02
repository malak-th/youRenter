from django import forms
from .models import Ware, Profile
from django.contrib.auth.models import User

class WareForm(forms.ModelForm):
    picture = forms.ImageField(required=False)
    class Meta:
        model = Ware
        fields = '__all__'
       
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['mobile', 'gender']
        
  
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)        