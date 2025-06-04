from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from base.models import Student, Seminar, SeminarGroup, SeminarRegistration


@login_required
def student_dashboard(request):
    try:
        student = request.user.student
    except Student.DoesNotExist:
        return redirect('login')

    # Registered seminars
    registered_seminars_qs = SeminarRegistration.objects.filter(student=student)
    registered_seminar_ids = registered_seminars_qs.values_list('seminar_id', flat=True)

    # Available seminars filtered by student's program and excluding registered ones
    all_unregistered = Seminar.objects.exclude(id__in=registered_seminar_ids)
    available_seminars = [s for s in all_unregistered if student.program in s.eligible_programs]

    # Seminar groups
    seminar_groups = SeminarGroup.objects.filter(students=student)

    context = {
        'student': student,
        'registered_seminars': registered_seminars_qs,
        'available_seminars': available_seminars,
        'seminar_groups': seminar_groups,
    }
    return render(request, 'students_templates/student_dashboard.html', context)


@login_required
def view_profile(request):
    student = get_object_or_404(Student, user=request.user)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, 'students_templates/includes/profile.html', {'student': student})
    return redirect('student_dashboard')


@login_required
def available_seminars(request):
    student = get_object_or_404(Student, user=request.user)

    # Filter in Python instead of DB
    seminars = [s for s in Seminar.objects.all() if student.program in s.eligible_programs]

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, 'students_templates/includes/seminars.html', {'seminars': seminars})

    return redirect('student_dashboard')




@login_required
def register_for_seminar(request, seminar_id):
    student = get_object_or_404(Student, user=request.user)
    seminar = get_object_or_404(Seminar, id=seminar_id)

    if student.program not in seminar.eligible_programs:
        msg = 'This seminar is not available for your program.'
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': msg})
        messages.error(request, msg)
        return redirect('student_dashboard')

    already_registered = SeminarRegistration.objects.filter(
        student=student,
        seminar__course_code=seminar.course_code
    ).exists()

    if already_registered:
        msg = f'You are already registered for the course: {seminar.course_code}'
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'info', 'message': msg})
        messages.warning(request, msg)
    else:
        SeminarRegistration.objects.create(student=student, seminar=seminar)
        msg = f'Successfully registered for seminar: {seminar.course_code}'
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': msg})
        messages.success(request, msg)

    return redirect('student_dashboard')



@login_required
def registered_seminars(request):
    student = get_object_or_404(Student, user=request.user)
    registered = SeminarRegistration.objects.filter(student=student)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, 'students_templates/includes/registered_seminars.html', {'registered_seminars': registered})

    return redirect('student_dashboard')


@login_required
def view_my_groups(request):
    student = get_object_or_404(Student, user=request.user)

    if not SeminarRegistration.objects.filter(student=student).exists():
        messages.warning(request, 'You must register for a seminar to view your group.')
        #return redirect('student_dashboard')

    groups = SeminarGroup.objects.filter(students=student)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, 'students_templates/includes/my_groups.html', {'groups': groups})

    return redirect('student_dashboard')
