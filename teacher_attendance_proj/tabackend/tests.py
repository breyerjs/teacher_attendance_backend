from django.test import TestCase
from rest_framework.test import APIRequestFactory
from tabackend.models import Teacher, School, Attendance
import json
from tabackend.views import password_correct, submit_attendance

# Create your tests here.

class TestSubmissions(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        home = School.objects.create(name="Home", city="McLean", latitude=38.946363, longitude=-77.221893)
        Teacher.objects.create(f_name='Jackson', l_name='Breyer', school=home, password='guest')

    def test_password_correct(self):
        body = {
            'f_name': 'Jackson',
            'l_name': 'Breyer',
            'school_name': 'Home',
            'entered_password': 'guest'
        }

        body_json = json.dumps(body)
        request = self.factory.post("/password_correct", data=body, format='json')
        response = password_correct(request)

        body_unicode = response.content.decode('utf-8')
        body = json.loads(body_unicode)

        self.assertTrue(body.get("password_correct"))

    def test_submit_attendance(self):
        body = {
            "f_name": "Jackson",
            "l_name": "Breyer",
            "school_name": "Home",
            "near_school": True,
            "phone_number": 2025551234,
        }

        body_json = json.dumps(body)
        request = self.factory.post("/submit_attendance", data=body, format='json')        
        response = submit_attendance(request)

        body_unicode = response.content.decode('utf-8')
        body = json.loads(body_unicode)

        #fix me
        print(body)