from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from .models import Review
<<<<<<< HEAD
=======
from .models import CustomUser, Review
>>>>>>> 7a713cc (skeleton : review system)
=======
>>>>>>> 383dd17 (base(add review) : working ✅)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'mobile_number', 'name', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['characteristic_1', 'characteristic_2', 'characteristic_3',
                  'characteristic_4', 'characteristic_5', 'characteristic_6',
                  'characteristic_7', 'feedback']
        widgets = {
            'characteristic_1': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'characteristic_2': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'characteristic_3': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'characteristic_4': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'characteristic_5': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'characteristic_6': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'characteristic_7': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'feedback': forms.Textarea(attrs={'rows': 4}),
<<<<<<< HEAD
        }
<<<<<<< HEAD
=======
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
>>>>>>> 7a713cc (skeleton : review system)
=======
>>>>>>> 383dd17 (base(add review) : working ✅)
=======
        }
>>>>>>> c226e4a (fallback commit - working ☑)
