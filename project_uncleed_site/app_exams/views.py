from django.shortcuts import render, redirect
from django.contrib.auth import login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from .models import Exam

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
