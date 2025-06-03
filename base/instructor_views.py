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
        form.instance.instructor = self.request.user.instructor
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


# Export Group Members to PDF
@login_required
def export_group_members(request, seminar_id):
    seminar = get_object_or_404(Seminar, id=seminar_id, instructor=request.user.instructor)
    groups = SeminarGroup.objects.filter(seminar=seminar).prefetch_related('students')

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - inch

    p.setFont("Helvetica-Bold", 14)
    p.drawString(inch, y, f"Seminar: {seminar.course_code}")
    y -= 0.5 * inch

    p.setFont("Helvetica", 12)

    for group in groups:
        p.drawString(inch, y, f"Group {group.group_number}:")
        y -= 0.3 * inch

        for student in group.students.all():
            full_name = student.user.get_full_name() or student.user.username
            p.drawString(inch + 0.3 * inch, y, f"- {full_name} ({student.registration_number})")
            y -= 0.25 * inch

            if y < inch:
                p.showPage()
                y = height - inch
                p.setFont("Helvetica", 12)

        y -= 0.2 * inch

    p.save()
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="seminar_{seminar.course_code}_groups.pdf"'
    return response
