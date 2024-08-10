from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter password'
    }))
  
    class Meta:
        model=Account
        fields=['full_name','email','password']

    



   