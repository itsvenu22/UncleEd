from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ReviewForm
from .models import Exam, MockTest, Review
from django.contrib.auth.decorators import login_required
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
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import Exam, MockTest, Review
from django.contrib.auth.decorators import login_required

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



def add_review(request, mock_test_id):
    mock_test = get_object_or_404(MockTest, pk=mock_test_id)
    
    # Ensure user is authenticated to add a review
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        description = request.POST.get('description')
        question_quality = request.POST.get('question_quality', 0)
        topic_hardness = request.POST.get('topic_hardness', 0)
        preparation_level = request.POST.get('preparation_level', 0)
        time_management = request.POST.get('time_management', 0)
        difficulty_balance = request.POST.get('difficulty_balance', 0)
        syllabus_coverage = request.POST.get('syllabus_coverage', 0)
        practical_relevance = request.POST.get('practical_relevance', 0)
        
        # Check if the student has already reviewed this mock test
        review_exists = Review.objects.filter(mock_test=mock_test, student=request.user).exists()

        if not review_exists:
            # Create a new review if not already created
            Review.objects.create(
                mock_test=mock_test,
                student=request.user,
                description=description,
                question_quality=question_quality,
                topic_hardness=topic_hardness,
                preparation_level=preparation_level,
                time_management=time_management,
                difficulty_balance=difficulty_balance,
                syllabus_coverage=syllabus_coverage,
                practical_relevance=practical_relevance,
            )
        else:
            # Update existing review
            review = Review.objects.get(mock_test=mock_test, student=request.user)
            review.description = description
            review.question_quality = question_quality
            review.topic_hardness = topic_hardness
            review.preparation_level = preparation_level
            review.time_management = time_management
            review.difficulty_balance = difficulty_balance
            review.syllabus_coverage = syllabus_coverage
            review.practical_relevance = practical_relevance
            review.save()

        return redirect('mock_test_detail', pk=mock_test.id)  # Adjust to your detail view name

    return render(request, 'add_review.html', {'mock_test': mock_test})

def mock_test_detail(request, pk):
    mock_test = get_object_or_404(MockTest, pk=pk)
    reviews = Review.objects.filter(mock_test=mock_test)

    # Check if the user wants to see only their own reviews
    if request.user.is_authenticated and 'my_reviews' in request.GET:
        reviews = reviews.filter(student=request.user)

    return render(request, 'mock_test_detail.html', {'mock_test': mock_test, 'reviews': reviews})

def mock_test_reviews(request, pk):
    mock_test = get_object_or_404(MockTest, pk=pk)
    reviews = Review.objects.filter(mock_test=mock_test)
    if request.user.is_authenticated and 'my_reviews' in request.GET:
        reviews = reviews.filter(student=request.user)
    return render(request, 'mock_test_reviews.html', {'mock_test': mock_test, 'reviews': reviews})