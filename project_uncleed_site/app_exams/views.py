from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ReviewForm
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

def exam_detail_view(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    mock_tests = exam.mock_tests.all()  # Get all mock tests related to this exam
    return render(request, 'exam_detail.html', {'exam': exam, 'mock_tests': mock_tests})

def contact(request):
    return render(request, 'contacts.html')

def notfound404(request):
    return render(request, 'notfound404.html')

@login_required
def add_review(request, mock_test_id):
    mock_test = get_object_or_404(MockTest, id=mock_test_id)
    exams = Exam.objects.all()
    mock_tests = MockTest.objects.all()
    # Check if the user has already reviewed this mock test
    existing_review = Review.objects.filter(mock_test=mock_test, user=request.user).first()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.mock_test = mock_test
            review.user = request.user
            review.save()
            return redirect('exam_detail', pk=mock_test.exam.id)  # Redirect to the respective exam page
    else:
        form = ReviewForm(instance=existing_review)
    
    return render(request, 'reviews/add_review.html', {'form': form, 'mock_test': mock_test, 'exam': exams, 'mock_tests': mock_tests})

