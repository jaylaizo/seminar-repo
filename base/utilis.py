from base.models import SeminarGroup

def try_group_students(seminar, student):
    """
    Assign a student to a group for a specific seminar.
    Each group holds up to 10 students. Automatically assigns
    the first student in a group as the group leader.
    """
    # Check if student is already in a group for this seminar
    existing_group = SeminarGroup.objects.filter(
        seminar=seminar,
        students=student
    ).first()

    if existing_group:
        return  # Student already grouped

    # Get the last created group for this seminar
    last_group = SeminarGroup.objects.filter(
        seminar=seminar
    ).order_by('-group_number').first()

    if not last_group or last_group.students.count() >= 10:
        # No group exists or last one is full → create a new group
        next_group_number = 1 if not last_group else last_group.group_number + 1
        group = SeminarGroup.objects.create(
            seminar=seminar,
            group_number=next_group_number
        )
    else:
        # Use the existing non-full group
        group = last_group

    group.students.add(student)

    # If this is the first student in the group, assign as leader
    if group.students.count() == 1:
        group.group_leader = student
        group.save()
