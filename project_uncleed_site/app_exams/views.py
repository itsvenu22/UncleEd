from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.shortcuts import render, get_object_or_404
from .models import Exam, MockTest
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('login')

def mock_test_detail(request, pk):
    mock_test = get_object_or_404(MockTest, pk=pk)
    if mock_test.is_premium and not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'mock_test_detail.html', {'mock_test': mock_test})

def home_view(request):
    exams = Exam.objects.all()
    mock_tests = MockTest.objects.all()

    return render(request, 'home.html', {'exams': exams, 'mock_tests': mock_tests})

def home_view(request):
    exams = Exam.objects.all()
    return render(request, 'home.html', {'exams': exams})

def exam_detail_view(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    mock_tests = exam.mock_tests.all()  # Get all mock tests related to this exam

    return render(request, 'exam_detail.html', {'exam': exam, 'mock_tests': mock_tests})

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    html_email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

def exam_detail_view(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    mock_tests = exam.mock_tests.all()
    return render(request, 'exam_detail.html', {'exam': exam, 'mock_tests': mock_tests})


def exam_detail_view(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    mock_tests = exam.mock_tests.all()
    return render(request, 'exam_detail.html', {'exam': exam, 'mock_tests': mock_tests})


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def contact(request):
    return render(request, 'contacts.html',)

def notfound404(request):
    return render(request, 'notfound404.html',)