from .data_access import DataAccess
"""
This file holds the business logic for the application.

"""
class Logic:
    def __init__(self):
        self.data_access = DataAccess()
        self.USER_EXISTS_ERROR = "A user with that username already exists."
        self.SCHOOL_DOES_NOT_EXIST_ERROR = "No school matches that name and city"

    def credentials_valid(self, request):
        user = self.data_access.get_user_by_username(request.username)
        if user is None:
            return False
        if not user.check_password(request.password):
            return False
        return True

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
