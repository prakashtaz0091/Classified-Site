from django import forms

from .models import Account, UserProfile


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter password"})
    )

    class Meta:
        model = Account
        fields = ["full_name", "email", "password"]


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = "__all__"
