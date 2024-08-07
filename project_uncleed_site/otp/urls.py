from django.urls import path
from .views import forgot_password, otp_verification

urlpatterns = [
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('otp-verification/', otp_verification, name='otp_verification'),
]
