from django import forms
from django.contrib.auth import login,authenticate,logout

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterFrom(UserCreationForm):
    email=forms.EmailField()
    employee_id = forms.CharField(max_length=100)
   
    class Meta:
        model= User
        fields=["employee_id","username","email","password1","password2"]

   