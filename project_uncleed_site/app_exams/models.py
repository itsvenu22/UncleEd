from django.contrib.auth.models import User
from django.db import models

class Exam(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name

class MockTest(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='mocktests')
    name = models.CharField(max_length=200)
    link = models.URLField()
    is_premium = models.BooleanField(default=False)  # New field for premium links

    def __str__(self):
        return self.name

User._meta.get_field('email')._unique = True
