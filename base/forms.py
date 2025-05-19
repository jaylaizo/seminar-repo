from django import forms
from django.contrib.auth.models import User
from .models import Student, Instructor, Venue, Seminar, SeminarRegistration, SeminarGroup

# This file contains forms for the models defined in the models.py file and it validates the data from the user templates 
# Form for creating/updating a User account (used in both student/instructor creation)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


# Student form
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['registration_number', 'phone_number']


# Instructor form
class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = []  # No extra fields apart from linked user


# Venue form
class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['venue_name', 'venue_capacity']


# Seminar form
class SeminarForm(forms.ModelForm):
    class Meta:
        model = Seminar
        fields = ['course_code', 'day', 'time', 'venue', 'instructor']


# Seminar registration form
class SeminarRegistrationForm(forms.ModelForm):
    class Meta:
        model = SeminarRegistration
        fields = ['student', 'seminar']


# Seminar Group form
class SeminarGroupForm(forms.ModelForm):
    class Meta:
        model = SeminarGroup
        fields = ['group_number', 'seminar', 'instructor', 'student']
        widgets = {
            'student': forms.CheckboxSelectMultiple(),  # for group assignment to multiple students 
        }
