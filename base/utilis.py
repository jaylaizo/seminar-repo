from base.models import SeminarGroup, SeminarRegistration

def try_group_students(seminar):
    """
    Automatically create groups of 10 students for a specific Seminar instance.
    Each seminar is uniquely defined by course_code, day, time, and venue.
    """
    # Get already grouped student IDs for this seminar
    grouped_ids = SeminarGroup.objects.filter(
        seminar=seminar
    ).values_list('students__id', flat=True)

    # Get ungrouped students registered for this exact seminar
    ungrouped_regs = SeminarRegistration.objects.filter(
        seminar=seminar
    ).exclude(student__id__in=grouped_ids).select_related('student') 

    ungrouped_students = [reg.student for reg in ungrouped_regs]

    if len(ungrouped_students) < 10:
        return  # Not enough students yet

    # Get the max existing group number for this seminar
    existing_numbers = SeminarGroup.objects.filter(seminar=seminar).values_list('group_number', flat=True)
    current_max = max(existing_numbers, default=0)

    # Create new groups of 10
    for i in range(0, len(ungrouped_students), 10):
        group_members = ungrouped_students[i:i + 10]
        if len(group_members) < 10:
            break  # Only full groups allowed

        current_max += 1
        group = SeminarGroup.objects.create(
            seminar=seminar,
            group_number=current_max
        )
        group.students.set(group_members)
