from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ReviewForm
from .models import Exam, MockTest, Review
from django.contrib.auth.decorators import login_required
<<<<<<< HEAD
>>>>>>> 7a713cc (skeleton : review system)
=======

<<<<<<< HEAD
>>>>>>> 383dd17 (base(add review) : working ✅)

=======
>>>>>>> e9f76cf (mock reviews with stars)
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
    
<<<<<<< HEAD
<<<<<<< HEAD
    # Ensure user is authenticated to add a review
    if not request.user.is_authenticated:
        return redirect('login')

<<<<<<< HEAD
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
>>>>>>> 7a713cc (skeleton : review system)
=======
    return render(request, 'reviews/add_review.html', {'form': form, 'mock_test': mock_test})
>>>>>>> 383dd17 (base(add review) : working ✅)
=======
    return render(request, 'reviews/add_review.html', {'form': form, 'mock_test': mock_test, 'exam': exams, 'mock_tests': mock_tests})
<<<<<<< HEAD
<<<<<<< HEAD

>>>>>>> 863ff91 (minor bug fixes)
=======
>>>>>>> c226e4a (fallback commit - working ☑)
=======

>>>>>>> 0a2f3fc (review page : complete ✅)
=======
@login_required
def user_reviews(request, mock_test_id):
    mock_test = get_object_or_404(MockTest, id=mock_test_id)
    # Fetch reviews by the current user for this mock test
    reviews = Review.objects.filter(mock_test=mock_test, user=request.user)
    star_range = [1, 2, 3, 4, 5]  # This will be used for star ratings

    return render(request, 'reviews/user_reviews.html', {
        'mock_test': mock_test,
        'reviews': reviews,
        'star_range': star_range,
        })

def all_reviews(request, mock_test_id):
    mock_test = get_object_or_404(MockTest, id=mock_test_id)
    reviews = Review.objects.filter(mock_test=mock_test)
    star_range = [1, 2, 3, 4, 5]  # This will be used for star ratings

    return render(request, 'reviews/all_reviews.html', {
        'mock_test': mock_test,
        'reviews': reviews,
        'star_range': star_range,  # Pass the star range to the template
    })
>>>>>>> e9f76cf (mock reviews with stars)
