from django.db import models
from django.contrib.auth.models import User

# Student Profile
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15)
    
    def __str__(self):
        return f"{self.user.username} ({self.registration_number})"


# Instructor Profile
class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


# Venue
class Venue(models.Model):
    venue_name = models.CharField(max_length=100)
    venue_capacity = models.IntegerField()

    def __str__(self):
        return self.venue_name


# Seminar
class Seminar(models.Model):
    course_code = models.CharField(max_length=20)
    time = models.TimeField()
    day = models.CharField(max_length=20)
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course_code} on {self.day} at {self.time}"


# Seminar Registration (Intermediate table for many-to-many Student-Seminar)
class SeminarRegistration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    seminar = models.ForeignKey(Seminar, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} registered for {self.seminar.course_code}"


# Seminar Group
class SeminarGroup(models.Model):
    group_number = models.IntegerField()
    seminar = models.ForeignKey(Seminar, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return f"Group {self.group_number} for {self.seminar.course_code}"

    class Meta:
        unique_together = ('seminar', 'group_number')
