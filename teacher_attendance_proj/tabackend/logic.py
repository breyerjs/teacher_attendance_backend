from .data_access import DataAccess
from django.contrib.auth.models import User
from django.http import HttpResponse
"""
This file holds the business logic for the application.

"""
class Logic:
    def create_user(self, request_body):
        if DataAccess().get_user_by_username(request_body.get('username')).count() >=1:
            return "A user with that username already exists."
        DataAccess().create_user(request_body)
        return None

    def credentials_valid(self, request):
        user = DataAccess().get_user_by_username(request.username)
        if user is None:
            return False
        if not user.check_password(request.password):
            return False
        return True
