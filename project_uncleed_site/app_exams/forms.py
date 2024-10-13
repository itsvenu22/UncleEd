from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Review

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'mobile_number', 'name', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'description', 'question_quality', 'topic_hardness', 'preparation_level',
            'time_management', 'difficulty_balance', 'syllabus_coverage', 'practical_relevance'
        ]
        widgets = {
            'question_quality': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'topic_hardness': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'preparation_level': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'time_management': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'difficulty_balance': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'syllabus_coverage': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'practical_relevance': forms.Select(choices=[(i, i) for i in range(1, 6)]),
        }
