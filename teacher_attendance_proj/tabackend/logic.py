from .data_access import DataAccess
from geopy.distance import vincenty
"""
This file holds the business logic for the application.

"""
class Logic:
    def __init__(self):
        self.data_access = DataAccess()
        self.USER_EXISTS_ERROR = "A user with that username already exists"
        self.SCHOOL_DOES_NOT_EXIST_ERROR = "No school matches that name and city"
        self.CREDENTIALS_INVALID_ERROR = "The credentials provided are incorrect"

    # private method
    def create_user(self, request_body):
        if self.data_access.get_user_by_username(request_body.get('username')) is not None:
            return self.USER_EXISTS_ERROR
        return self.data_access.create_user(request_body)

    def create_teacher(self, request_body):
        user = self.create_user(request_body)
        if user == self.USER_EXISTS_ERROR:
            return user
        # get school
        school = self.data_access.get_school(name=request_body.get('school_name'), 
                                            city=request_body.get('school_city'))
        if school is None:
            return self.SCHOOL_DOES_NOT_EXIST_ERROR

        self.data_access.create_teacher(user=user, school=school)
        return None

    def submit_attendance(self, request):
        username = request.get('username')
        password = request.get('password')
        latitude = request.get('latitude')
        longitude = request.get('longitude')
        phone_number = request.get('phone_number')

        if not self.teacher_credentials_valid(username, password):
            return self.CREDENTIALS_INVALID_ERROR
        teacher = self.data_access.get_teacher_by_username(username)
        near_school = self.is_near_school(latitude, longitude, teacher.school)
        attendance_today = self.data_access.get_check_ins_today(teacher)
        # If no check-ins today, record attendance
        if attendance_today.count() == 0:
            self.data_access.create_attendance(teacher, near_school, phone_number)
            return
        # If check in today is near school, do nothing
        if attendance_today.filter(near_school=True).count() > 0:
            return
        # Check in today must not be near school
        if near_school:
            self.data_access.create_attendance(teacher, near_school, phone_number)
        else:
            return

    # 'Near' is defined as 'within a mile of'
    def is_near_school(self, latitude, longitude, school):
        school_loction = (school.latitude, school.longitude)
        teacher_location = (latitude, longitude)
        return vincenty(teacher_location, school_loction).miles <= 1

    def teacher_credentials_valid(self, username, password):
        user = self.data_access.get_teacher_by_username(username)
        if user is None:
            return False
        if not user.check_password(password):
            return False
        return True
