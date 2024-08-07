from django.shortcuts import render, redirect
from django.contrib.auth import login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from .models import Exam
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import ForgotPasswordForm
from otp.models import OTP
from django.contrib.auth.models import User
from otp.forms import ForgotPasswordForm

def exam_list(request):
    exams = Exam.objects.all()
    return render(request, 'app_exams/exam_list.html', {'exams': exams})

def mocktest_list(request, exam_id):
    exam = Exam.objects.get(id=exam_id)
    if request.user.is_authenticated:
        mocktests = exam.mocktests.all()
    else:
        mocktests = exam.mocktests.filter(is_premium=False)
    return render(request, 'app_exams/mocktest_list.html', {'exam': exam, 'mocktests': mocktests})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('exam_list')
    else:
        form = SignUpForm()
    return render(request, 'app_exams/signup.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('exam_list')

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