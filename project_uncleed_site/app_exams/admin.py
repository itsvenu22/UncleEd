from django.contrib import admin
from .models import CustomUser, Exam, MockTest

from django.contrib import admin
from .models import Review

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'mobile_number']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Exam)
admin.site.register(MockTest)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'mock_test', 'get_exam_title', 'created_at')

    def get_exam_title(self, obj):
        return obj.mock_test.exam.title
    get_exam_title.short_description = 'Exam Title'

admin.site.register(Review, ReviewAdmin)