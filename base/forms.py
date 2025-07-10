from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Instructor, Venue, Seminar, SeminarRegistration, SeminarGroup, PROGRAM_CHOICES

# Constants
DAYS_OF_WEEK = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
]
TIME_SLOTS = [
    (f"{hour:02d}:00-{hour+1:02d}:00", f"{hour:02d}:00–{hour+1:02d}:00")
    for hour in range(7, 20)
]


# --- Registration Forms ---

class StudentRegistrationForm(UserCreationForm):
    registration_number = forms.CharField(max_length=13, help_text="Unique identifier for students")
    phone_number = forms.CharField(max_length=15)
    program = forms.ChoiceField(choices=PROGRAM_CHOICES)  

    class Meta: 
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'registration_number', 'phone_number', 'program'] 

class InstructorRegistrationForm(UserCreationForm):
    check_number = forms.CharField(
        max_length=8,
        help_text="Unique identifier for instructors"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['check_number'].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user  # Save Instructor separately in the view



# --- Admin Update Forms ---

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['registration_number', 'phone_number', 'program']

class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ['check_number']  


# --- Venue Form ---

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['venue_name', 'venue_capacity']
        widgets = {
            'venue_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter venue name'}),
            'venue_capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter capacity'}),
        }




# --- Instructor Seminar Creation Form ---

class AddSeminarForm(forms.ModelForm):
    day = forms.ChoiceField(
        choices=DAYS_OF_WEEK,
        label="Day",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    time = forms.ChoiceField(
        choices=TIME_SLOTS,
        label="Time",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    venue = forms.ModelChoiceField(
        queryset=Venue.objects.all(),
        label="Venue",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    eligible_programs = forms.MultipleChoiceField(
        choices=PROGRAM_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Eligible Programs"
    )

    class Meta:
        model = Seminar
        fields = ['course_code', 'day', 'time', 'venue', 'eligible_programs']
        widgets = {
            'course_code': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_eligible_programs(self):
        return self.cleaned_data['eligible_programs']

    def clean(self):
        cleaned_data = super().clean()
        venue = cleaned_data.get('venue')
        day = cleaned_data.get('day')
        time = cleaned_data.get('time')

        if venue and day and time:
            conflict = Seminar.objects.filter(
                venue=venue,
                day=day,
                time=time
            ).exists()

            if conflict:
                raise forms.ValidationError("This venue is already booked for the selected day and time.")

# --- Seminar Registration ---

class SeminarRegistrationForm(forms.ModelForm):
    class Meta:
        model = SeminarRegistration
        fields = ['student', 'seminar']


# --- Seminar Group ---

class SeminarGroupForm(forms.ModelForm):
    class Meta:
        model = SeminarGroup
        fields = ['group_number', 'seminar', 'instructor', 'students']
        widgets = {
            'students': forms.CheckboxSelectMultiple(),  # fix key typo from "student"
        }
        
class SeminarWorkUploadForm(forms.ModelForm):
    class Meta:
        model = SeminarGroup
        fields = ['seminar_file']
        widgets = {
            'seminar_file': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }

class MarksUploadForm(forms.ModelForm):
    class Meta:
        model = SeminarGroup
        fields = ['marks']
        widgets = {
            'marks': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
        }
