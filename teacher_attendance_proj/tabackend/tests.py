from django.test import TestCase
from rest_framework.test import APIRequestFactory
from tabackend.models import Teacher, School, Attendance
import json
from tabackend.views import password_correct, submit_attendance

# Create your tests here.

class TestSubmissions(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.home = School.objects.create(name="Home", city="McLean", latitude=38.946363, longitude=-77.221893)
        self.teacher = Teacher.objects.create(f_name='Jackson', l_name='Breyer', school=self.home, password='guest')

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

    def test_successful_submit_attendance(self):
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

        # record saved
        self.assertEqual(len(Attendance.objects.filter(teacher=self.teacher)), 1)

        # correct response
        self.assertTrue(body.get("first_submission_today"))

    def test_unsuccessful_submit_attendance(self):
        # ie if there are two submissions on the same day
        body = {
            "f_name": "Jackson",
            "l_name": "Breyer",
            "school_name": "Home",
            "near_school": True,
            "phone_number": 2025551234,
        }

        body_json = json.dumps(body)
        request1 = self.factory.post("/submit_attendance", data=body, format='json')        
        response1 = submit_attendance(request1)

        request2 = self.factory.post("/submit_attendance", data=body, format='json')        
        response2 = submit_attendance(request2)

        body_unicode = response2.content.decode('utf-8')
        body = json.loads(body_unicode)

        # second record NOT saved
        self.assertEqual(len(Attendance.objects.filter(teacher=self.teacher)), 1)

        # correct response
        self.assertFalse(body.get("first_submission_today"))        




