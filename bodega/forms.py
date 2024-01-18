from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control campo'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control campo'}))