
from django.shortcuts import render
from django.http import HttpResponse
from .models import Admin, Student, Lecture, User, Semester


def semester_manage(req):
    li = Semester.objects.all()

    return render(req, "semester_manage.html", {"li": li})


def semester_add(req):
    year = req.POST.get("year")
    semester = req.POST.get("semester")

    Semester.objects.create(year=year,
                            semester=semester).save()

    return HttpResponse("Add semester ok!")


