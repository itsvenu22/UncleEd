from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
import string

class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)

    def is_expired(self):
        return (timezone.now() - self.created_at).total_seconds() > 300  # 5 minutes

    @staticmethod
    def generate_otp():
        return ''.join(random.choices(string.digits, k=6))
