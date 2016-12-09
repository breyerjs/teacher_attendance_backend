
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from tabackend.models import Teacher, School, Attendance
import json
from tabackend.views import submit_attendance
from .logic import Logic



class TestSubmissions(TestCase):

    def setUp(self):
        self.USERNAME = "Alobar"
        self.PASSWORD = "panpanpan"

        self.create_teacher_request_body = {
            'username': self.USERNAME,
            'email': 'jitterbug@perfume.com',
            'password': self.PASSWORD,
            'firstName': 'Alobar',
            'lastName': 'Pan',
            'isSuperUser': False,
            'school_name': 'Embarcadero',
            'school_city': 'San Francisco'
        }



        self.factory = APIRequestFactory()
        self.school = School.objects.create(
            name="Embarcadero", 
            city="San Francisco", 
            latitude=37.799263, 
            longitude=-122.397673)
        self.teacher = Logic().create_teacher(self.create_teacher_request_body)
        self.location_near_school = (38.946363, -77.221893)
        self.location_not_near_school = (11.572076, 43.145647)

    def test_submit_attendance_near_school_first_time_saves_properly(self):
        body = {
            'username': self.USERNAME,
            'password': self.PASSWORD,
            "latitude": self.location_near_school[0],
            "longitude": self.location_near_school[1],
            "phone_number": '2021234567'
        }
        request = self.factory.post("/submit_attendance", data=body, format='json')
        response = submit_attendance(request)
        self.assertEquals(response.status_code, 204)
