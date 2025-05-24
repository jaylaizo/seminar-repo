from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from base.models import Student, Seminar, SeminarGroup, SeminarRegistration
from django.contrib import messages 


# Student Dashboard    
@login_required
def student_dashboard(request):
    try: 
        student = request.user.student 
    except Student.DoesNotExist: 
        return redirect('login')

    registered_seminars = SeminarRegistration.objects.filter(student=student).values_list('seminar_id', flat=True) #
    available_seminars = Seminar.objects.exclude(id__in=registered_seminars) 
    registered = SeminarRegistration.objects.filter(student=student) 
    seminar_groups = SeminarGroup.objects.filter(student=student) 

    context = {
        'student': student,
        'available_seminars': available_seminars,
        'registered_seminars': registered,
        'seminar_groups': seminar_groups,
    }
    return render(request, 'students_templates/student_dashboard.html', context) 


# View Student Profile
@login_required
def view_profile(request):
    student = get_object_or_404(Student, user=request.user)
    return render(request, 'students_templates/profile.html', {'student': student})


# View All Available Seminars
@login_required
def available_seminars(request):
    seminars = Seminar.objects.all()
    return render(request, 'students_templates/available_seminars.html', {'seminars': seminars})


# Register for a Seminar
@login_required
def register_for_seminar(request, seminar_id):
    student = get_object_or_404(Student, user=request.user)
    seminar = get_object_or_404(Seminar, id=seminar_id)

    if SeminarRegistration.objects.filter(student=student, seminar=seminar).exists():
        messages.info(request, 'You are already registered for this seminar.')
    else:
        SeminarRegistration.objects.create(student=student, seminar=seminar)
        messages.success(request, f'Registered for seminar: {seminar.course_code}')

    return redirect('available_seminars')


# View Group(s) Only If Student Is Registered
@login_required
def view_my_groups(request):
    student = get_object_or_404(Student, user=request.user)
    if not SeminarRegistration.objects.filter(student=student).exists():
        messages.warning(request, 'You must register for a seminar to view your group.')
        return redirect('available_seminars')

    groups = SeminarGroup.objects.filter(student=student)
    return render(request, 'students_templates/my_groups.html', {'groups': groups})
