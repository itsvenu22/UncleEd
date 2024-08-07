from django.urls import path
from .views import exam_list, mocktest_list, signup, logout

urlpatterns = [
    path('', exam_list, name='exam_list'),
    path('exam/<int:exam_id>/', mocktest_list, name='mocktest_list'),
    path('signup/', signup, name='signup'),
    path('logout/', logout, name='logout'),
]
