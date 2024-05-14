from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Admin, Student, Lecture


# Create your views here.
def index(request):
    # return HttpResponse("This is the first att!")
    return render(request, "login_page.html")


def login(request):
    acc = request.POST.get("acc")
    pw = request.POST.get("pw")
    role = request.POST.get("role")

    if role == "admin":
        result = Admin.objects.filter(admin_id=acc, password=pw)
    elif role == "lecture":
        result = Lecture.objects.filter(staff_id=acc, password=pw)
    else:
        result = Student.objects.filter(student_id=acc, password=pw)

    if not result:
        return HttpResponse("ERROR: login failed!")

    result = result[0]  #

    request.session["ROLE"] = role


    if role == "admin":
        id = result.admin_id
    elif role == "lecture":
        id = result.staff_id
    else:
        id = result.student_id

    request.session["LOGIN_ID"] = id
    # request.se

    return redirect("/home")

    # return HttpResponse("执行登录逻辑~")


def home(req):
    return render(req, "home_page.html")
