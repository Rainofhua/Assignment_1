
from django.shortcuts import render
from django.http import HttpResponse
from .models import Admin, Student, Lecture, User


def customers_manage(req):
    li = User.objects.all()

    return render(req, "user_manage.html", {"li": li})
