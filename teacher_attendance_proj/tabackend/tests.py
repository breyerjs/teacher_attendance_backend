
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from tabackend.models import School, Attendance
from tabackend.views import submit_attendance
from .logic import Logic



class TestSubmissions(TestCase):

    def setUp(self):
        self.USERNAME = "Alobar"
        self.PASSWORD = "panpanpan"
        self.NOT_THE_PASSWORD = "wam bam kablam"

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
        self.location_near_school = (37.799263, -122.397673)
        self.location_not_near_school = (11.572076, 43.145647)

        self.near_school_request_body = {
            'username': self.USERNAME,
            'password': self.PASSWORD,
            "latitude": self.location_near_school[0],
            "longitude": self.location_near_school[1],
            "phone_number": '2021234567'
        }

        self.not_near_school_request_body = {
            'username': self.USERNAME,
            'password': self.PASSWORD,
            "latitude": self.location_not_near_school[0],
            "longitude": self.location_not_near_school[1],
            "phone_number": '2021234567'
        }

    def test_submit_attendance_near_school_first_time_saves(self):
        body = self.near_school_request_body
        request = self.factory.post("/submit_attendance", data=body, format='json')
        response = submit_attendance(request)
        attendance = Attendance.objects.filter(teacher__username=self.USERNAME).first()
        self.assertTrue(attendance.near_school)
        self.assertEquals(response.status_code, 204)

    def test_submit_attendance_not_near_school_first_time_saves(self):
        body = self.not_near_school_request_body
        request = self.factory.post("/submit_attendance", data=body, format='json')
        response = submit_attendance(request)
        attendance = Attendance.objects.filter(teacher__username=self.USERNAME).first()
        self.assertFalse(attendance.near_school)
        self.assertEquals(response.status_code, 204)        

    def test_submit_attendance_not_near_school_then_near_school_saves_both(self):
        # not near school
        body = self.not_near_school_request_body
        request = self.factory.post("/submit_attendance", data=body, format='json')
        response = submit_attendance(request)
        self.assertEquals(response.status_code, 204)        

        # near school
        body = self.near_school_request_body
        request = self.factory.post("/submit_attendance", data=body, format='json')
        response = submit_attendance(request)
        self.assertEquals(response.status_code, 204)        
        attendances = Attendance.objects.filter(teacher__username=self.USERNAME)
        self.assertEqual(1, attendances.filter(near_school=True).count())
        self.assertEqual(1, attendances.filter(near_school=False).count())

    def test_submit_attendance_twice_near_school_saves_once(self):
        # near school
        body = self.near_school_request_body
        request = self.factory.post("/submit_attendance", data=body, format='json')
        response = submit_attendance(request)
        self.assertEquals(response.status_code, 204) 

        # near school
        body = self.near_school_request_body
        request = self.factory.post("/submit_attendance", data=body, format='json')
        response = submit_attendance(request)
        self.assertEquals(response.status_code, 400) 
        self.assertEqual(1, Attendance.objects.filter(teacher__username=self.USERNAME).count())

    def test_submit_attendance_near_school_then_not_near_school_saves_first_only(self):
        # near school
        body = self.near_school_request_body
        request = self.factory.post("/submit_attendance", data=body, format='json')
        response = submit_attendance(request)
        self.assertEquals(response.status_code, 204)    

        # not near school
        body = self.not_near_school_request_body
        request = self.factory.post("/submit_attendance", data=body, format='json')
        response = submit_attendance(request)
        self.assertEquals(response.status_code, 400)         
        attendances = Attendance.objects.filter(teacher__username=self.USERNAME)
        self.assertEqual(1, attendances.count())
        self.assertTrue(attendances.first().near_school)

    def test_submit_not_near_school_then_not_near_school_saves_once(self):
        # not near school
        body = self.not_near_school_request_body
        request = self.factory.post("/submit_attendance", data=body, format='json')
        response = submit_attendance(request)
        self.assertEquals(response.status_code, 204)         

        # not near school
        body = self.not_near_school_request_body
        request = self.factory.post("/submit_attendance", data=body, format='json')
        response = submit_attendance(request)
        self.assertEquals(response.status_code, 204)         
        self.assertEquals(1, Attendance.objects.filter(teacher__username=self.USERNAME).count())

    def test_submit_incorrect_credentials_returns_401(self):
        body = self.near_school_request_body
        body['password'] = self.NOT_THE_PASSWORD
        request = self.factory.post("/submit_attendance", data=body, format='json')
        response = submit_attendance(request)
        self.assertEquals(response.status_code, 401) 
