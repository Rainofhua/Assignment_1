from django.db import models


# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.CharField(max_length=128, unique=True)


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    dob = models.DateTimeField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=128)
    classs = models.ForeignKey(to='Class', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.student_id) + str(self.dob)


class Lecture(models.Model):
    staff_id = models.AutoField(primary_key=True)
    dob = models.DateTimeField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=128)


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    dob = models.DateTimeField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=128)


class Semester(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.IntegerField()
    semester = models.CharField(max_length=128)


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=128)
    name = models.CharField(max_length=128)


class Class(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField()
    course = models.ForeignKey(to='Course', on_delete=models.CASCADE, null=True)
    semester = models.ForeignKey(to="Semester", on_delete=models.CASCADE, null=True)
    lecture = models.ForeignKey(to="Lecture", on_delete=models.CASCADE, null=True)


class CollegeDay(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    classs_id = models.IntegerField()


class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    link_college_day = models.ForeignKey(to="CollegeDay", on_delete=models.CASCADE)
    ## 0:Skip / 1:Normal / 2:Leave / 3:Late
    state = models.IntegerField()
    link_stu = models.ForeignKey(to="Student", on_delete=models.CASCADE)
