from django.http import HttpResponse, JsonResponse
from tabackend.models import School, Teacher, Attendance
from django.template import RequestContext, loader
from django.utils import timezone
from .mobile_tools import MobileTools
from .logic import Logic
import json

"""
TODO:
    1. Generate report for report view.
"""

# ===================================================== #
# WEB API

"""
Accepts:
{
 'username': str,
 'password': str,
 'email': str (optional),
 'firstName': str,
 'lastName': str,
}

 returns:
 204
"""
def create_user(request):
    if request.method != 'POST':
        return HttpResponse(status=405)
    error = Logic().create_user(get_request_body(request))
    if isinstance(error, str):
        return HttpResponse(error, status=500)
    else:
        return HttpResponse(status=204)


"""
{
  "username": "jacksonnnn",
  "email":  "jbreeyer@practicefusion.com",
  "password": "guest",
  "firstName": "Jackson",
  "lastName": "Breyer",
  "isSuperUser": false,
  "school_name": "Home",
  "school_city": "McLean"
}
"""
def create_teacher(request):
    if request.method != 'POST':
        return HttpResponse(status=405)
    error = Logic().create_teacher(get_request_body(request))
    if error:
        return HttpResponse(error, status=500)
    else:
        return HttpResponse(status=204)


    """
    TODO.
    Passes in:
        all_schools{
            "Brandeis": {
                "Jackson Breyer": 45
            }
        }
    ...where the main dict maps the school's name to an inner dict.
        The inner dict maps each teacher name to the number of times
        that teacher has been reported missing.
    """
def report(request):
    tools = MobileTools()
    attendance = tools.get_all_teachers_num_times_present()
    template = loader.get_template('tabackend/report.html')
    context = RequestContext(request, {'attendance': attendance})
    return HttpResponse(template.render(context))

# ===================================================== #
# MOBILE API

def login(request):
    if not Logic.credentials_valid(get_request_body(request)):
        return HttpResponse(status=403)
    return HttpResponse(status=204)


"""
returns:
    {
        "school": [list of teacher names],
        ...
    }
"""
def get_all_schools_and_teachers(request):
    response = {school.name: [] for school in School.objects.all()}
    for teacher in Teacher.objects.all():
        name = teacher.f_name + " " + teacher.l_name
        response[teacher.school.name].append(name)

    return (JsonResponse(response))


"""
Requires:
    {
        "f_name": "Jackson",
        "l_name": "Breyer",
        "school_name": "Brandeis",
        "near_school": True,
        "phone_number": 2025551234,
        "password":
    }

Returns:
    {
        "submission_successful": true
    }
"""
def submit_attendance(request):

    tools = MobileTools()
    body = tools.get_request_body(request)

    teacher = Teacher.objects.get(f_name=body.get("f_name"),
                                  l_name=body.get("l_name"),
                                  school__name=body.get("school_name")
                                  )

    # create + save the new Attendance object, if reporter hasn't reported today
    if not tools.teacher_submitted_today(teacher):
        Attendance.objects.create(
            date=timezone.now(),
            near_school=body.get("near_school"),
            teacher=teacher,
            phone_number=body.get("phone_number")
        )
        return JsonResponse({"submission_successful": True})

    # if the teacher has already checked in today
    #   see mobile_tools for sanitation policy
    else:
        tools.deduplicate_entries(request)
        return JsonResponse({"submission_successful": True})


"""
requires:
    {
        password:
        school_name: "Brandeis"
    }

returns:
    {
        latitude: 38.933868
        longitude: -77.177260
    }

"""
def get_lat_long(request):
    school = School.objects.get(name=request.get("school_name"))
    return JsonResponse(
        {
            "latitude": school.latitude,
            "longitude": school.longitude
        })

# ===================================================== #
# HELPER METHODS

def get_request_body(request):
    body_unicode = request.body.decode('utf-8')
    return json.loads(body_unicode)
