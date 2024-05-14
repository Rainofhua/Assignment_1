
from django.shortcuts import render
from django.http import HttpResponse
from .models import Admin, Student, Lecture, User, Semester, Course


def course_manage(req):
    li = Course.objects.all()
    return render(req, "course_manage.html", {"li": li})


def course_add(req):
    code = req.POST.get("code")
    name = req.POST.get("name")

    Course.objects.create(code=code,
                          name=name).save()

    return HttpResponse("Add Course ok!")
