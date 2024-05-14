
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Admin, Student, Lecture, User, Attendance


def students_manage(req):
    li = Student.objects.all()

    return render(req, "student_manage.html", {"li": li})


def students_add(req):
    first_name = req.POST.get("first_name")
    last_name = req.POST.get("last_name")
    email = req.POST.get("email")
    dob = req.POST.get("dob")
    password = req.POST.get("password")

    User.objects.create(first_name=first_name,
                        last_name=last_name,
                        email=email).save()

    last_id = User.objects.last().id

    Student.objects.create(
        dob=dob,
        user=User.objects.get(id=last_id),
        password=password,
    ).save()

    return HttpResponse("Add lecture ok!")


def edit_student(req):
    id = req.GET.get("id")
    info = Student.objects.get(student_id=id)

    dob = info.dob
    if dob:
        # info.dob = "2002-10-11"
        try:
            info.dob = dob.strftime('%Y-%m-%d')
        except Exception as e:
            info.dob = "2002-10-10"
    else:
        info.dob = "2002-10-10"

    return render(req, "edit_student.html", {"info": info})


def exe_edit_student(req):
    id = req.POST.get("id")
    first_name = req.POST.get("first_name")
    last_name = req.POST.get("last_name")
    birth = req.POST.get("dob")
    email = req.POST.get("email")

    stu = Student.objects.filter(student_id=id)
    uid = stu[0].user.id
    User.objects.filter(id=uid).update(
        first_name=first_name,
        last_name=last_name,
        email=email
    )

    stu.update(
        dob=birth
    )

    return redirect("/students_manage")


def remove_stu_from_class(req):
    sid = req.GET.get("sid")
    cid = req.GET.get("cid")
    print(sid)
    Attendance.objects.filter(link_stu_id=sid).delete()
    Student.objects.filter(student_id=sid).update(classs_id=None)
    return redirect("/view_students_list?cid=" + cid)
