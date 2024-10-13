from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)
    name = models.CharField(max_length=100)

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile_number']

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
    link = models.URLField(max_length=255, default="youtube.com")
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Review(models.Model):
    mock_test = models.ForeignKey(MockTest, related_name='reviews', on_delete=models.CASCADE)
    student = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)

    # 7 Individual Star Ratings with 5-star max per criterion
    question_quality = models.PositiveIntegerField(default=0)
    topic_hardness = models.PositiveIntegerField(default=0)
    preparation_level = models.PositiveIntegerField(default=0)
    time_management = models.PositiveIntegerField(default=0)
    difficulty_balance = models.PositiveIntegerField(default=0)
    syllabus_coverage = models.PositiveIntegerField(default=0)
    practical_relevance = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('mock_test', 'student')

    def __str__(self):
        return f"{self.student.name} - {self.mock_test.title}"

    @property
    def average_rating(self):
        total_stars = sum([
            self.question_quality, self.topic_hardness, self.preparation_level,
            self.time_management, self.difficulty_balance, self.syllabus_coverage,
            self.practical_relevance
        ])
        return total_stars / 7.0  # Average across all seven criteria
