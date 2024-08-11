from django.contrib import admin
from .models import CustomUser, Exam, MockTest

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'mobile_number']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Exam)
admin.site.register(MockTest)
