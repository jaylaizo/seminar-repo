from django.db import models
from django.contrib.auth.models import User


#Student Profile
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15)
    

    def register_seminar(self):
        pass

    def view_group(self):
        pass

    def view_seminar_detail(self):
        pass

# Instructor Profile
class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def view_group(self):
        pass

    def print_group_name(self):
        pass


#Venue
class Venue(models.Model):
    venue_name = models.CharField(max_length=100)
    venue_capacity = models.IntegerField()

    def get_venue_name(self):
        return self.venue_name

    def get_venue_capacity(self):
        return self.venue_capacity

#Seminar
class Seminar(models.Model):
    course_code = models.CharField(max_length=20)
    time = models.TimeField()
    day = models.CharField(max_length=20)
    student = models.ForeignKey(Student,  on_delete=models.SET_NULL, null=True)
    instructor= models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

    def register_student(self):
        pass

    def assign_venue(self):
        pass
    
    def __str__(self):
        return f"{self.course_code} on {self.day} at {self.time}"

# Registration Model (Intermediate for Student and Seminar)
class SeminarRegistration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    seminar = models.ForeignKey(Seminar, on_delete=models.CASCADE )
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} registered for {self.seminar.course_code}"


# Seminar Group
class SeminarGroup(models.Model):
    group_number = models.IntegerField()
    seminar=models.ForeignKey(Seminar, on_delete=models.CASCADE)
    instructor=models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True)
    student=models.ManyToManyField(Student)
    

    def auto_schedule_group(self):
        pass
    def __str__(self):
        return f" Group {self.group_number} " 
