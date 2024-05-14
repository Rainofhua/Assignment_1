
from django.contrib import admin
from django.urls import path
from app import views, students_views, customers_views, lecturer_views, semester_views, course_views, class_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index),
    path("login", views.login),
    path("home", views.home),
    path("students_manage", students_views.students_manage),
    path("edit_student", students_views.edit_student),
    path("exe_edit_student", students_views.exe_edit_student),
    path("remove_stu_from_class", students_views.remove_stu_from_class),
    path("customers_manage", customers_views.customers_manage),
    path("students_add", students_views.students_add),
    path("lecture_manage", lecturer_views.lecture_manage),
    path("lecture_add", lecturer_views.lecture_add),
    path("lecture_check_class", lecturer_views.lecture_check_class),
    path("semester_add", semester_views.semester_add),
    path("semester_manage", semester_views.semester_manage),
    path("course_manage", course_views.course_manage),
    path("course_add", course_views.course_add),
    path("class_add", class_views.class_add),
    path("class_manage", class_views.class_manage),
    path("view_students_list", class_views.view_students_list),
    path("enroll_stu", class_views.enroll_stu),
    path("college_day_manage", class_views.college_day_manage),
    path("add_college_day", class_views.add_college_day),
    path("save_attendance", class_views.save_attendance),
    path("check_attendance", class_views.check_attendance),
    path("send_mail", class_views.send_mail),
    path("students_batch_upload", class_views.students_batch_upload),
]
