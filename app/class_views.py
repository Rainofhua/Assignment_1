
from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Admin, Student, Lecture, User, Semester, Class, Course, CollegeDay, Attendance
from datetime import date
from datetime import datetime, timedelta
import time
#import xlrd
import os


def class_manage(req):
    li = Class.objects.all()

    all_Semester = Semester.objects.all()
    all_Lecture = Lecture.objects.all()
    all_Course = Course.objects.all()
    return render(req, "class_manage.html", {"li": li,
                                             "all_Semester": all_Semester,
                                             "all_Lecture": all_Lecture,
                                             "all_Course": all_Course,
                                             "isAdmin": True
                                             })


def class_add(req):
    number = req.POST.get("number")
    course_id = req.POST.get("course_id")
    semester_id = req.POST.get("semester_id")
    lecture_id = req.POST.get("lecture_id")

    Class.objects.create(number=number,
                         course_id=course_id,
                         semester_id=semester_id,
                         lecture_id=lecture_id,
                         ).save()

    return HttpResponse("Add class ok!")


def view_students_list(req):
    cid = req.GET.get("cid")
    s = Student.objects.filter(classs_id=cid)
    ow = datetime.now().strftime('%Y-%m-%d')
    cdd = CollegeDay.objects.filter(classs_id=cid, date=ow)
    if cdd:
        cdd = cdd[0].id
    else:
        cdd = None
    li = []
    all_state = {
        0: "Skip",
        1: "Normal",
        2: "Leave",
        3: "Late",
    }
    for so in s:
        ssid = so.student_id
        ssname = so.user.first_name + "-" + so.user.last_name
        ssp = so.password
        sse = so.user.email
        so_info = {
            "ssid": ssid,
            "ssname": ssname,
            "ssp": ssp,
            "sse": sse
        }
        state = None
        if cdd:
            app = Attendance.objects.filter(link_college_day_id=cdd, link_stu_id=ssid)
            if app:
                app = app[0]
                state = app.state
        so_info["state"] = state
        so_info["state_text"] = all_state[state] if state in (0,1,2,3) else "NOT RECORDED "

        li.append(so_info)

    # query no class student
    sno = Student.objects.filter(Q(classs_id__isnull=True))

    cl = Class.objects.get(id=cid)

    ct = CollegeDay.objects.filter(classs_id=cid, date=ow)
    if ct:
        ct_id = ct[0].id
    else:
        ct_id = None
    ct = ct.count()
    having_class = "YES" if ct > 0 else "NO"
    role = req.session["ROLE"]
    data = {"s": li, "sno": sno, "cid": cid, "class_info": cl, "today_date": ow, "having_class": having_class,
            "ct_id": ct_id, "role": role}

    return render(req, "view_students_list.html", data)


def enroll_stu(req):
    stu_id = req.POST.get("stu_id")
    cid = req.POST.get("cid")

    Student.objects.filter(student_id=stu_id).update(classs_id=cid)
    return HttpResponse("enroll ok!")


def college_day_manage(req):
    cid = req.GET.get("cid")
    cgd = CollegeDay.objects.filter(classs_id=cid)
    return render(req, "college_day_manage.html", {"cgd": cgd, "cid": cid})


def add_college_day(req):
    cid = req.GET.get("cid")
    date = req.GET.get("date")

    ct = CollegeDay.objects.filter(classs_id=cid, date=date).count()
    if ct > 0:
        return HttpResponse("There are already classes on this day")
    print(date)

    CollegeDay.objects.create(classs_id=cid, date=date).save()

    return HttpResponse(" college day saved")


def save_attendance(req):
    cid = req.GET.get("cid")
    ct_id = req.GET.get("ct_id")
    stu_id = req.GET.get("stu_id")
    state = req.GET.get("state")

    record = Attendance.objects.filter(
        link_college_day_id=ct_id, link_stu_id=stu_id
    )
    if record:
        record.update(state=state)
    else:
        Attendance.objects.create(
            link_college_day_id=ct_id, link_stu_id=stu_id, state=state
        )
    return redirect("/view_students_list?cid=" + cid)


def check_attendance(req):
    cid = req.GET.get("cid")
    sid = req.GET.get("sid")


    if not cid:
        sog = Student.objects.filter(student_id=sid)
        if sog:
            cid = sog[0].classs_id
        else:
            return HttpResponse("You have not been registered in any class yet!")


    cgd = CollegeDay.objects.filter(classs_id=cid)
    total_ok = 0
    all_state = {
        0: "Skip",
        1: "Normal",
        2: "Leave",
        3: "Late",
    }
    li = []
    for c in cgd:
        dt = c.date
        cdid = c.id

        record = Attendance.objects.filter(
            link_college_day_id=cdid, link_stu_id=sid
        )
        if record:
            record = record[0].state
            record_text = all_state[record]

            total_ok += 1
        else:
            record_text = "NOT RECORDED"
        di = {
            "date": dt,
            "record_text": record_text
        }
        li.append(di)

    if total_ok == 0 or len(li) == 0:
        percent = "0.00"

    else:
        percent = round(total_ok / len(li) * 100)

    return render(req, "check_attendance.html",
                  {"li": li, "lilen": len(li), "total_ok": total_ok, "percent": percent, "sid": sid})


def send_mail(req):
    from django.conf import settings
    from django.core.mail import send_mail

    # sid={{ sid }}&ead={{ lilen }}&aad={{ total_ok }}&p={{ percent }}
    sid = req.GET.get("sid")
    ead = req.GET.get("ead")
    aad = req.GET.get("aad")
    p = req.GET.get("p")

    su = Student.objects.get(student_id=sid).user
    name = su.first_name + "-" + su.last_name

    msg = 'Dear {}, <br/>You are expected to be attendance for {} days this semester, ' \
          'but you have only been present for {} day, ' \
          'with a attendance rate of {}%. ' \
          'Please contact your lecturer after receiving the message;'

    msg = msg.format(name, ead, aad, p)
    send_mail('POOR ATTENDANCE !!', '', settings.EMAIL_FROM,
              [su.email],
              html_message=msg)
    return HttpResponse('email has sent!')


def students_batch_upload(req):

    file_handle = req.FILES.get('excel')

    filename = str(time.time()) + file_handle.name

    destination = open("./static/files/" + filename, "wb+")
    for chunk in file_handle.chunks():
        destination.write(chunk)
    destination.close()

    file_xlsx = xlrd.open_workbook(os.getcwd() + '/static/files/' + filename)

    all_sheet = file_xlsx.sheets()

    sheet1 = all_sheet[0]

    sheet1_rows = sheet1.nrows
    value_list = []
    t = 0
    for i in range(1, sheet1_rows):
        if sheet1.row_values(i):
            sr = sheet1.row_values(i)

            if User.objects.filter(email=sr[2]).count() > 0:
                continue

            User.objects.create(first_name=sr[0],
                                last_name=sr[1],
                                email=sr[2]).save()

            last_id = User.objects.last().id

            Student.objects.create(
                dob=sr[3],
                user=User.objects.get(id=last_id),
                password=str(sr[4]),
            ).save()
            t += 1
    return HttpResponse("%d students's info saved, duplicate student's emails will be skipped;!" % t)
