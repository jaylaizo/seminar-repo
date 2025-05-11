from django.contrib import admin
from .models import*

#Registered  models
admin.site.register(Venue)
admin.site.register(Seminar)
admin.site.register(Student)
admin.site.register(SeminarGroup)
admin.site.register(Instructor)
admin.site.register(SeminarRegistration)




