from django.contrib.auth.models import User
"""
This file holds the logic for accessing the database.
It's essentially a set of stored procedures but wtiten with
the Django ORM
"""

class DataAccess:

    def create_user(self, request_body):
        User.objects.create_user(username=request_body.get('username'), 
                                email=request_body.get('email'),
                                password=request_body.get('password'),
                                first_name=request_body.get('firstName'),
                                last_name=request_body.get('lastName'))

    def get_user_by_username(self, username):
        user = User.objects.filter(username=username)
        if user.count() == 0:
            return None
        return user.first()
