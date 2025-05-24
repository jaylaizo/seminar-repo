from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Instructor, Venue, Seminar, SeminarRegistration, SeminarGroup

# --- User creation with extra fields for registration ---

class StudentRegistrationForm(UserCreationForm):
    registration_number = forms.CharField(max_length=20)
    phone_number = forms.CharField(max_length=15)

    class Meta: 
        model = User
        fields = ['username', 'email', 'password1', 'password2']  

class InstructorRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']




# User form (can be used for admin-level updates)
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


# Student form (used by admin or in a multi-step registration)
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['registration_number', 'phone_number']


# Instructor form (no extra fields)
class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = []


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


# Seminar group form
class SeminarGroupForm(forms.ModelForm):
    class Meta:
        model = SeminarGroup
        fields = ['group_number', 'seminar', 'instructor', 'students']
        widgets = {
            'student': forms.CheckboxSelectMultiple(),
        }
