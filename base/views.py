from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView
from .forms import StudentRegistrationForm, InstructorRegistrationForm
from base.models import Student, Instructor



# Login view
class UserLoginView(FormView):
    template_name = 'main/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('student_dashboard')  # Default; will override dynamically

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        # Redirect based on role
        if hasattr(user, 'student'):
            return redirect('student_dashboard')
        elif hasattr(user, 'instructor'):
            return redirect('instructor_dashboard')  # Create later
        else:
            return redirect('admin:index')




# Logout view
class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('login')


class StudentRegisterView(FormView):
    template_name = 'students_templates/student_register.html'
    form_class = StudentRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        Student.objects.create(
            user=user,
            registration_number=form.cleaned_data['registration_number'],
            phone_number=form.cleaned_data['phone_number'],
            program=form.cleaned_data['program']
        )
        messages.success(self.request, 'Student registered successfully.')
        return redirect(self.get_success_url())


class InstructorRegisterView(FormView):
    template_name = 'instructors_templates/instructor_register.html'
    form_class = InstructorRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        Instructor.objects.create(user=user)
        user=user,
        check_number=form.cleaned_data['check_number'],
        messages.success(self.request, 'Instructor registered successfully.')
        return redirect(self.get_success_url())
