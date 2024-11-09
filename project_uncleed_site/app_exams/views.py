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
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 383dd17 (base(add review) : working ✅)

=======
>>>>>>> e9f76cf (mock reviews with stars)
=======
from django.db.models import Avg

=======
from django.db.models import Avg, F
import json
>>>>>>> e7e63bc (fallback : sorting working ✅)

>>>>>>> 3908468 (fallback : whole review for exams)
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
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> e9f76cf (mock reviews with stars)
=======


=======
>>>>>>> 5a9e7ba (fallback : sorting headless done ✅)
def combined_reviews_view(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    mock_tests = MockTest.objects.filter(exam=exam)

    # Get the characteristic to sort by, defaulting to overall rating
    sort_by = request.GET.get('sort_by', 'overall')

    # Get the number of top mock tests to show
    show_count = request.GET.get('show_count', '5')

    # Validate show_count input
    if show_count in ['5', '7', '10']:
        show_count = int(show_count)
    else:
        show_count = float('inf')  # 'all' case

    # Overall sorting calculation
    if sort_by == 'overall':
        top_mock_tests = (
            mock_tests.annotate(
                avg_rating=(F('reviews__characteristic_1') + 
                            F('reviews__characteristic_2') + 
                            F('reviews__characteristic_3') + 
                            F('reviews__characteristic_4') + 
                            F('reviews__characteristic_5') + 
                            F('reviews__characteristic_6') + 
                            F('reviews__characteristic_7')
                ) / 7  # Average of all characteristics
            ).annotate(avg_rating=Avg('avg_rating'))
            .order_by('-avg_rating')
        )
    else:
        # Validate the sorting field
        valid_sort_fields = [
            'characteristic_1', 'characteristic_2', 'characteristic_3',
            'characteristic_4', 'characteristic_5', 'characteristic_6', 
            'characteristic_7'
        ]

        if sort_by not in valid_sort_fields:
            sort_by = 'characteristic_1'  # Default sorting field if invalid

        top_mock_tests = (
            mock_tests.annotate(avg_rating=Avg(f'reviews__{sort_by}'))
            .order_by('-avg_rating')
        )

    # Adjust the queryset based on show_count
    if show_count != float('inf'):
        top_mock_tests = top_mock_tests[:show_count]

    # Select only the top 2 mock tests for the radar chart
    top_2_mock_tests = top_mock_tests[:2]

    combined_reviews = {}
    radar_data = {
        'labels': [
            "Clarity of Concepts",
            "Difficulty Appropriateness",
            "Relevance to Exam Pattern",
            "Quality of Questions",
            "Time Management",
            "Overall Preparation Value",
            "Likelihood of Recommending"
        ],
        'datasets': []
    }

    for mock_test in top_2_mock_tests:
        reviews = Review.objects.filter(mock_test=mock_test)

        avg_reviews = {
            'avg_clarity': reviews.aggregate(Avg('characteristic_1'))['characteristic_1__avg'] or 0,
            'avg_difficulty': reviews.aggregate(Avg('characteristic_2'))['characteristic_2__avg'] or 0,
            'avg_relevance': reviews.aggregate(Avg('characteristic_3'))['characteristic_3__avg'] or 0,
            'avg_quality': reviews.aggregate(Avg('characteristic_4'))['characteristic_4__avg'] or 0,
            'avg_time_management': reviews.aggregate(Avg('characteristic_5'))['characteristic_5__avg'] or 0,
            'avg_preparation_value': reviews.aggregate(Avg('characteristic_6'))['characteristic_6__avg'] or 0,
            'avg_recommendation': reviews.aggregate(Avg('characteristic_7'))['characteristic_7__avg'] or 0,
        }

        radar_data['datasets'].append({
            'label': mock_test.title,
            'data': list(avg_reviews.values()),
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'borderWidth': 1
        })

        combined_reviews[mock_test.id] = avg_reviews

# this is for testing only
        temp = {
            "characteristic_1" : "avg_clarity",
            "characteristic_2" : "avg_difficulty",
            "characteristic_3" : "avg_relevance",
            "characteristic_4" : "avg_quality",
            "characteristic_5" : "avg_time_management",
            "characteristic_6" : "avg_preparation_value",
            "characteristic_7" : "avg_recommendation"
        }

    context = {
        'exam': exam,
        'top_mock_tests': top_mock_tests,
        'mock_tests': mock_tests,
        'combined_reviews': combined_reviews,
        'radar_data_json': json.dumps(radar_data),
        'sort_by': sort_by,
        'show_count': show_count,
        'temp': temp
    }
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    
    # Debugging context
    print("Context data:", context)
    
    return render(request, 'reviews/combined_reviews.html', context)
>>>>>>> 3908468 (fallback : whole review for exams)
=======
    return render(request, 'reviews/combined_reviews.html', context)
>>>>>>> b947e0c (fallback : exam analytics ✅)
=======
    return render(request, 'reviews/combined_reviews.html', context)
>>>>>>> e7e63bc (fallback : sorting working ✅)
=======
    return render(request, 'reviews/combined_reviews.html', context)
>>>>>>> 23eb7c9 (fallback : sorting ✅ (combined review for an exam))
=======
    return render(request, 'reviews/combined_reviews.html', context)
>>>>>>> 5a9e7ba (fallback : sorting headless done ✅)
