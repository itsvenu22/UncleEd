from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ReviewForm
from .models import Exam, MockTest, Review
from django.contrib.auth.decorators import login_required

from django.db.models import Avg, F
import json

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

def about(request):
    return render(request, 'about.html')

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
    return render(request, 'reviews/combined_reviews.html', context)
from django.shortcuts import render, get_object_or_404
from django.db.models import Avg
from .models import Exam, MockTest, Review
import json

def mock_test_comparison(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    mock_tests = MockTest.objects.filter(exam=exam)

    # Chart type selection (default to radar)
    chart_type = request.GET.get('chart_type', 'radar')

    # Get selected mock tests for comparison
    mock_test_1_id = request.GET.get('mock_test_1')
    mock_test_2_id = request.GET.get('mock_test_2')

    # Default to first 2 mock tests if not selected
    selected_mocks = mock_tests[:2]
    if mock_test_1_id and mock_test_2_id:
        selected_mocks = mock_tests.filter(id__in=[mock_test_1_id, mock_test_2_id])[:2]

    # Prepare data structure for chart
    labels = [
        "Clarity of Concepts", "Difficulty Appropriateness", "Relevance to Exam Pattern",
        "Quality of Questions", "Time Management", "Overall Preparation Value",
        "Likelihood of Recommending"
    ]

    radar_data = {
        'labels': labels,
        'datasets': []
    }
    bar_line_data = {
        'labels': labels,
        'bar_datasets': [],
        'line_datasets': []
    }

    # Populate radar and bar/line datasets
    for mock in selected_mocks:
        reviews = Review.objects.filter(mock_test=mock)
        avg_reviews = [
            reviews.aggregate(Avg(f'characteristic_{i}'))[f'characteristic_{i}__avg'] or 0
            for i in range(1, 8)
        ]

        # Add dataset for radar chart
        radar_data['datasets'].append({
            'label': mock.title,
            'data': avg_reviews,
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'borderWidth': 1
        })

        # Add datasets for bar and line charts
        bar_line_data['bar_datasets'].append({
            'label': mock.title,
            'data': avg_reviews,
            'backgroundColor': 'rgba(153, 102, 255, 0.6)',
            'borderColor': 'rgba(153, 102, 255, 1)',
            'borderWidth': 1
        })
        bar_line_data['line_datasets'].append({
            'label': mock.title,
            'data': avg_reviews,
            'fill': False,
            'borderColor': 'rgba(255, 99, 132, 1)',
            'tension': 0.1
        })

    # Pass the prepared data to the template
    context = {
        'exam': exam,
        'mock_tests': mock_tests,
        'chart_type': chart_type,
        'selected_mock_1': mock_test_1_id,
        'selected_mock_2': mock_test_2_id,
        'radar_data_json': json.dumps(radar_data),
        'bar_line_data_json': json.dumps(bar_line_data)
    }
    return render(request, 'reviews/mock_comparison.html', context)
