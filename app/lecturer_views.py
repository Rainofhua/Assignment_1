
from django.shortcuts import render
from django.http import HttpResponse
from .models import Admin, Student, Lecture, User, Class


def lecture_manage(req):
    return render(req, "lecture_manage.html", {"li": Lecture.objects.all()})


def lecture_add(req):
    first_name = req.POST.get("first_name")
    last_name = req.POST.get("last_name")
    email = req.POST.get("email")
    dob = req.POST.get("dob")
    password = req.POST.get("password")

    User.objects.create(first_name=first_name,
                        last_name=last_name,
                        email=email).save()

    last_id = User.objects.last().id

    Lecture.objects.create(
        dob=dob,
        user=User.objects.get(id=last_id),
        password=password,
    ).save()

    return HttpResponse("Add student ok!")


def lecture_check_class(req):
    login_id = req.session["LOGIN_ID"]
    li = Class.objects.filter(lecture_id=login_id)
    return render(req, "class_manage.html", {"li": li, "isAdmin":False})