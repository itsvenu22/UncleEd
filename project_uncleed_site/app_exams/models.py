from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)
    name = models.CharField(max_length=100)
    
    username = None  # Remove the username field or set it to None
    USERNAME_FIELD = 'email'  # Set email as the username field
    REQUIRED_FIELDS = ['name', 'mobile_number']  # Other required fields

    def __str__(self):
        return self.email

class Exam(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)

    def __str__(self):
        return self.title

class MockTest(models.Model):
    exam = models.ForeignKey(Exam, related_name='mock_tests', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.title
