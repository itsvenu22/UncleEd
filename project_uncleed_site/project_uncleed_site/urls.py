from django.contrib import admin
from django.urls import path
from app_exams import views
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView
from django.conf.urls import handler404

handler404 = 'app_exams.views.notfound404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('404/', views.notfound404, name='notfound404'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('exam/<int:pk>/', views.exam_detail_view, name='exam_detail'),
    path('mocktest/<int:mock_test_id>/review/', views.add_review, name='add_review'),
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    path('exam/<int:pk>/', views.mock_test_detail, name='mock_test_detail'),  # Added this line
=======
    path('exam/<int:mock_test_id>/add_review/', views.add_review, name='add_review'),
    path('mock_test/<int:pk>/', views.mock_test_detail, name='mock_test_detail'),
    path('mock_test/<int:pk>/reviews/', views.mock_test_reviews, name='mock_test_reviews'),
>>>>>>> 7a713cc (skeleton : review system)
=======
    path('mocktest/<int:pk>/', views.mock_test_detail, name='mock_test_detail'),
>>>>>>> 383dd17 (base(add review) : working ✅)
=======
    path('mocktest/<int:mock_test_id>/your-reviews/', views.user_reviews, name='user_reviews'),  # Added line
=======
    path('mocktest/<int:mock_test_id>/your-reviews/', views.user_reviews, name='user_reviews'),
>>>>>>> 9077692 (fallback - new version ✅ (minor updates))
    path('mocktest/<int:pk>/', views.mock_test_detail, name='mock_test_detail'),
    path('mocktest/<int:mock_test_id>/all-reviews/', views.all_reviews, name='all_reviews'),
    path('exam/<int:exam_id>/combined-reviews/', views.combined_reviews_view, name='combined_reviews'),
    path('exam/<int:exam_id>/mock-comparison/', views.mock_test_comparison, name='mock_comparison'),

>>>>>>> e9f76cf (mock reviews with stars)
]
