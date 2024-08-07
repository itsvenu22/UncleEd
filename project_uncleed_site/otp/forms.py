from django import forms
from django.contrib.auth.models import User

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()

class ResetPasswordForm(forms.Form):
    otp_code = forms.CharField(max_length=6)
    new_password = forms.CharField(widget=forms.PasswordInput)
