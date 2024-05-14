from django.contrib import admin

from app.models import User,Class,Course,Lecture,Semester,Admin,Attendance,CollegeDay
# Register your models here.
admin.site.register(User)
admin.site.register(Class)
admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Semester)
admin.site.register(Admin)
admin.site.register(Attendance)
admin.site.register(CollegeDay)