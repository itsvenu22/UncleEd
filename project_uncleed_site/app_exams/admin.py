from django.contrib import admin
from .models import Exam, MockTest

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(MockTest)
class MockTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'exam', 'link')
    list_filter = ('exam',)
