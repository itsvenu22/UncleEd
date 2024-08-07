from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.conf import settings
from .models import OTP
from .forms import ForgotPasswordForm, ResetPasswordForm
from django.contrib.auth.forms import PasswordChangeForm

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                otp_code = OTP.generate_otp()
                OTP.objects.update_or_create(user=user, defaults={'otp_code': otp_code})
                send_mail(
                    'Your OTP Code',
                    f'Your OTP code is: {otp_code}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                )
                return redirect('otp_verification')
            except User.DoesNotExist:
                form.add_error('email', 'No user with this email address.')
    else:
        form = ForgotPasswordForm()
    return render(request, 'otp/forgot_password.html', {'form': form})

def otp_verification(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp_code']
            new_password = form.cleaned_data['new_password']
            try:
                otp = OTP.objects.get(otp_code=otp_code)
                if otp.is_expired():
                    form.add_error('otp_code', 'OTP has expired.')
                else:
                    user = otp.user
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)
                    otp.delete()
                    return redirect('login')
            except OTP.DoesNotExist:
                form.add_error('otp_code', 'Invalid OTP code.')
    else:
        form = ResetPasswordForm()
    return render(request, 'otp/otp_verification.html', {'form': form})
