from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from .views import UserLoginView, UserLogoutView, StudentRegisterView, InstructorRegisterView, InstructorRegisterView
from .teaching_timetable_view import TeachingTimetableView
from .instructor_views import InstructorDashboardView, SeminarGroupMembersView, export_group_members, AddSeminarView, \
    InstructorSeminarsView, RegisteredStudentsView, export_registered_students
from . import student_views
from . import instructor_views
from .venue_views import add_venue

urlpatterns = [
    path('', lambda request: redirect('login', permanent=False)),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    path('add-venue/', add_venue, name='add_venue'),

    # instructor-related URLs
    path('instructor/dashboard/', InstructorDashboardView.as_view(), name='instructor_dashboard'),
    path('instructor/add-seminar/', AddSeminarView.as_view(), name='add_seminar'),
    path('instructor/seminars/', InstructorSeminarsView.as_view(), name='seminar_list'),
    path('instructor/seminar/<int:seminar_id>/registered/', RegisteredStudentsView.as_view(),
         name='registered_students'),
    path('instructor/seminar/<int:seminar_id>/groups/', SeminarGroupMembersView.as_view(), name='seminar_groups'),
    path('instructor/seminar/<int:seminar_id>/submissions/', instructor_views.view_seminar_submissions,
         name='view_submissions'),
    path('instructor/group/<int:group_id>/upload-marks/', instructor_views.upload_group_marks,
         name='upload_group_marks'),
    path('instructor/seminar/<int:seminar_id>/export/', export_group_members, name='export_group_members'),
    path('instructor/export-registered/<int:seminar_id>/', export_registered_students,
         name='export_registered_students'),
    path('register/instructor/', InstructorRegisterView.as_view(), name='instructor_register'),

    # student-related URLs
    path('upload_pdf/', TeachingTimetableView.as_view(), name='upload_pdf'),
    path('register/student/', StudentRegisterView.as_view(), name='student_register'),
    path('student/dashboard/', student_views.student_dashboard, name='student_dashboard'),
    path('student/profile/', student_views.view_profile, name='view_profile'),
    path('student/seminars/', student_views.available_seminars, name='available_seminars'),
    path('student/seminar/register/<int:seminar_id>/', student_views.register_for_seminar, name='register_seminar'),
    path('student/registered-seminars/', student_views.registered_seminars, name='registered_seminars'),
    path('student/groups/', student_views.view_my_groups, name='my_groups'),
    path('student/group/<int:group_id>/upload/', student_views.upload_seminar_work, name='upload_seminar_work'),

]
