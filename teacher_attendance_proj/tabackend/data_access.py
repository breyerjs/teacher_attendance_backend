from django.contrib.auth.models import User
from .models import Teacher, School, Attendance
from datetime import datetime

"""
This file holds the logic for accessing the database.
It's essentially a set of stored procedures but wtiten with
the Django ORM
"""

class DataAccess:

    def create_user(self, request_body):
        user = User.objects.create_user(username=request_body.get('username'), 
                                email=request_body.get('email'),
                                password=request_body.get('password'),
                                first_name=request_body.get('firstName'),
                                last_name=request_body.get('lastName'))
        return user

    def create_teacher(self, user, school):
        # funny syntax because we're subclassing from User
        teacher = Teacher(user_ptr_id=user.id, school=school)
        teacher.__dict__.update(user.__dict__)
        teacher.save()
        return teacher

    def create_attendance(self, teacher, near_school, phone_number):
        return Attendance.objects.create(teacher=teacher,
                                    near_school=near_school,
                                    date_submitted=datetime.utcnow(),
                                    phone_number=phone_number)

    def get_user_by_username(self, username):
        user = User.objects.filter(username=username)
        if user.count() == 0:
            return None
        return user.first()

    def get_teacher_by_username(self, username):
        teacher = Teacher.objects.filter(username=username)
        if teacher.count() == 0:
            return None
        return teacher.first()        

    def get_school(self, name, city):
        school = School.objects.filter(name=name, 
                                    city=city)
        if school.count() == 0:
            return None
        return school.first()

    def get_check_ins_today(self, teacher):
        today = datetime.utcnow().date()
        return Attendance.objects.filter(teacher__username=teacher.username,
                                        date_submitted__date=today)
