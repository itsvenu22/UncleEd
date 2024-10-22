from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a `CustomUser` with an email, and password."""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)
    name = models.CharField(max_length=100)

    username = None  # Remove the username field or set it to None
    USERNAME_FIELD = 'email'  # Set email as the username field
    REQUIRED_FIELDS = ['name', 'mobile_number']  # Other required fields

    objects = CustomUserManager()  # Use the custom user manager

    def __str__(self):
        return self.email


class Exam(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, default="No description provided")

    def __str__(self):
        return self.title


class MockTest(models.Model):
    exam = models.ForeignKey(Exam, related_name='mock_tests', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    link = models.URLField(max_length=255, default="https://youtube.com")
    description = models.TextField(null=True, default="No description provided")
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Review(models.Model):
    mock_test = models.ForeignKey(MockTest, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Rating fields
    characteristic_1 = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    characteristic_2 = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    characteristic_3 = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    characteristic_4 = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    characteristic_5 = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    characteristic_6 = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    characteristic_7 = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('mock_test', 'user')

    def __str__(self):
        return f"Review by {self.user.username} for {self.mock_test.title} (Exam: {self.mock_test.exam.title})"
