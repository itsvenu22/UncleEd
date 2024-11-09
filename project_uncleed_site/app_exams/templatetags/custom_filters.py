# app_exams/templatetags/my_custom_filters.py
from django import template

register = template.Library()

@register.filter
def to(value, arg):
    # Define the logic you want here
    return str(value) + str(arg)
