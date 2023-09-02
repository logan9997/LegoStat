from django import forms
from config import ModelValidations as MV

class Login(forms.Form):
    username = forms.CharField(max_length=MV.Lengths.USERNAME)
    password = forms.CharField(max_length=MV.Lengths.PASSWORD)


class SignUp(forms.Form):
    username = forms.CharField(max_length=MV.Lengths.USERNAME)
    password = forms.CharField(max_length=MV.Lengths.PASSWORD)
    password_confirmation = forms.CharField(max_length=MV.Lengths.PASSWORD)
