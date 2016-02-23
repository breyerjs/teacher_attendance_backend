from django.test import TestCase
from rest_framework.test import APIRequestFactory
from tabackend.models import Teacher, School, Attendance
import json
from tabackend.views import password_correct

# Create your tests here.

class TestSubmissions(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        home = School.objects.create(name="Home", city="McLean", latitude=1.0, longitude=1.0)
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
