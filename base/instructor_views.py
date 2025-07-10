from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.template.loader import render_to_string
from django.views import View
from base.forms import AddSeminarForm
from base.models import Seminar, SeminarGroup, Instructor
from .forms import MarksUploadForm
from django.contrib import messages
from django.shortcuts import redirect

from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch


# Instructor Dashboard
class InstructorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'instructors_templates/instructor_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            instructor = self.request.user.instructor
        except Instructor.DoesNotExist:
            context['error'] = "You are not assigned as an instructor."
            return context
        context['seminars'] = Seminar.objects.filter(instructor=instructor)
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            # Return only the content for AJAX
            return render(self.request, 'instructors_templates/includes/dashboard_content.html', context)
        return super().render_to_response(context, **response_kwargs)


# Add Seminar View
class AddSeminarView(LoginRequiredMixin, CreateView):
    model = Seminar
    form_class = AddSeminarForm
    template_name = 'instructors_templates/includes/add_seminar.html'
    success_url = reverse_lazy('instructor_dashboard')

    def form_valid(self, form):
        instructor = self.request.user.instructor
        day = form.cleaned_data['day']
        time = form.cleaned_data['time']
        venue = form.cleaned_data['venue']

        if Seminar.objects.filter(day=day, time=time, venue=venue).exists():
            form.add_error('venue', "This venue is already taken for the selected day and time. Please choose another.")
            return self.form_invalid(form)

        form.instance.instructor = instructor
        return super().form_valid(form)

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return render(self.request, 'instructors_templates/includes/add_seminar.html', context)
        return super().render_to_response(context, **response_kwargs)


# Instructor Seminars View
class InstructorSeminarsView(View):
    def get(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            seminars = Seminar.objects.filter(instructor=request.user.instructor)
            return render(request, 'instructors_templates/includes/seminars_list.html', {
                'seminars': seminars
            })
        
        return render(request, 'instructors_templates/instructor_dashboard.html')


# Seminar Groups View
class SeminarGroupMembersView(LoginRequiredMixin, TemplateView):
    template_name = 'instructors_templates/includes/seminar_groups.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seminar_id = self.kwargs['seminar_id']
        seminar = get_object_or_404(Seminar, id=seminar_id, instructor=self.request.user.instructor)
        groups = SeminarGroup.objects.filter(seminar=seminar).prefetch_related('students')
        context['seminar'] = seminar
        context['groups'] = groups
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return render(self.request, 'instructors_templates/includes/seminar_groups.html', context)
        return super().render_to_response(context, **response_kwargs)


class RegisteredStudentsView(LoginRequiredMixin, TemplateView):
    template_name = 'instructors_templates/includes/registered_students.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seminar_id = self.kwargs['seminar_id']
        seminar = get_object_or_404(Seminar, id=seminar_id, instructor=self.request.user.instructor)

        # Fetch all students registered for this seminar (regardless of groups)
        registered_students = seminar.seminarregistration_set.select_related('student__user')

        context['seminar'] = seminar
        context['registered_students'] = [reg.student for reg in registered_students]
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return render(self.request, self.template_name, context)
        return super().render_to_response(context, **response_kwargs)

# View Seminar_work Submissions
@login_required
def view_seminar_submissions(request, seminar_id):
    seminar = get_object_or_404(Seminar, id=seminar_id, instructor=request.user.instructor)
    groups = SeminarGroup.objects.filter(seminar=seminar).exclude(seminar_file='')

    return render(request, 'instructors_templates/includes/view_submissions.html', {'seminar': seminar, 'groups': groups})

# Upload Group Marks
@login_required
@login_required
def upload_group_marks(request, group_id):
    group = get_object_or_404(SeminarGroup, id=group_id, seminar__instructor=request.user.instructor)

    if request.method == 'POST':
        form = MarksUploadForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, f"Marks uploaded for Group {group.group_number}.")
            return redirect('view_submissions', seminar_id=group.seminar.id)
        else:
            # Return the form with errors if it's submitted via AJAX
            return render(request, 'instructors_templates/includes/upload_marks.html', {
                'form': form,
                'group': group
            })
    else:
        form = MarksUploadForm(instance=group)
        return render(request, 'instructors_templates/includes/upload_marks.html', {
            'form': form,
            'group': group
        })

# Export Registered Students to PDF
@login_required
def export_registered_students(request, seminar_id):
    seminar = get_object_or_404(Seminar, id=seminar_id, instructor=request.user.instructor)
    registered_students = seminar.seminarregistration_set.select_related('student__user')

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    styles = getSampleStyleSheet()
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 50, f"Registered Students for {seminar.course_code} - {seminar.day} at {seminar.time}")

    data = [["Name", "Registration Number", "Phone Number"]]

    for reg in registered_students:
        student = reg.student
        name = student.user.get_full_name() or student.user.username
        data.append([name, student.registration_number, student.phone_number])

    # Create table
    table = Table(data, colWidths=[200, 150, 150])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
    ]))

    # Calculate Y-position
    table.wrapOn(p, width, height)
    table_height = 20 * len(data)  # rough estimate
    y = height - 80

    if y - table_height < 40:
        p.showPage()
        y = height - 40

    table.drawOn(p, 50, y - table_height)

    p.showPage()
    p.save()
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    filename = f'registered_students_{seminar.course_code}.pdf'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


# Export Group Members to PDF

@login_required
def export_group_members(request, seminar_id):
    seminar = get_object_or_404(Seminar, id=seminar_id, instructor=request.user.instructor)
    groups = SeminarGroup.objects.filter(seminar=seminar).prefetch_related('students')

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    styles = getSampleStyleSheet()
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 50, f"Seminar Groups for {seminar.course_code} - {seminar.day} at {seminar.time}")

    y_position = height - 80

    for group in groups:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y_position, f"Group {group.group_number}")
        y_position -= 20

        data = [["Name", "Registration Number", "Phone Number"]]
        for student in group.students.all():
            name = student.user.get_full_name() or student.user.username
            data.append([name, student.registration_number, student.phone_number])

        table = Table(data, colWidths=[200, 150, 150])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ]))

        table_width, table_height = table.wrap(0, 0)
        if y_position - table_height < 50:
            p.showPage()
            y_position = height - 50
            p.setFont("Helvetica-Bold", 12)
            p.drawString(50, y_position, f"Group {group.group_number}")
            y_position -= 20

        table.drawOn(p, 50, y_position - table_height)
        y_position -= table_height + 30

    p.showPage()
    p.save()
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="seminar_{seminar.course_code}_groups.pdf"'
    return response
