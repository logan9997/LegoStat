from django import forms
from config import ModelValidations as MV

class Login(forms.Form):
    username = forms.CharField(max_length=MV.Lengths.USERNAME)
    password = forms.CharField(max_length=MV.Lengths.PASSWORD)


class SignUp(forms.Form):
    username = forms.CharField(max_length=MV.Lengths.USERNAME)
    password = forms.CharField(max_length=MV.Lengths.PASSWORD)
    password_confirmation = forms.CharField(max_length=MV.Lengths.PASSWORD)


class UpdatePortfolioIten(forms.Form):
    date_bought = forms.DateField(required=False)
    date_sold = forms.DateField(required=False)
    bought_for = forms.DecimalField(required=False, min_value=0)
    sold_for = forms.DecimalField(required=False, min_value=0)
    notes = forms.CharField(required=False, max_length=MV.Lengths.NOTES)