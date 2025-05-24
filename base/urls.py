from django.urls import path
from django.contrib.auth import views as auth_views 
from . views import UserLoginView, UserLogoutView, StudentRegisterView, InstructorRegisterView 
from .seminar_views import TeachingTimetableView


from . import student_views
urlpatterns = [
    
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/student/', StudentRegisterView.as_view(), name='student_register'),
    path('register/instructor/', InstructorRegisterView.as_view(), name='instructor_register'),
    
    path('upload_pdf/',TeachingTimetableView.as_view(), name='upload_pdf'),
    path('student/dashboard/', student_views.student_dashboard, name='student_dashboard'),
    path('student/profile/', student_views.view_profile, name='view_profile'),
    path('student/seminars/', student_views.available_seminars, name='available_seminars'),
    path('student/seminar/register/<int:seminar_id>/', student_views.register_for_seminar, name='register_for_seminar'),
    path('student/groups/', student_views.view_my_groups, name='view_my_groups'),
]

