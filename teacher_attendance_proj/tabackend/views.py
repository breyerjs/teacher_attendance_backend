from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from tabackend.models import School, Teacher, Attendance
from django.template import RequestContext, loader
from django.utils import timezone
from .mobile_tools import MobileTools
from django.views.decorators.csrf import csrf_exempt
import json

"""
TODO:
    1. Generate report for report view.
"""

# ===================================================== #
# WEB API


def report(request):
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
    tools = MobileTools()
    attendance = tools.get_all_teachers_num_times_missing()
    template = loader.get_template('tabackend/report.html')
    context = RequestContext(request, {'attendance': attendance})
    return HttpResponse(template.render(context))

# ===================================================== #
# MOBILE API


def get_all_schools_and_teachers(request):
    """
    requires:
        {
            "password":
        }

    returns:
        {
            "school": [list of teacher names],
            ...
        }
    """

    response = {school.name: [] for school in School.objects.all()}
    for teacher in Teacher.objects.all():
        name = teacher.f_name + " " + teacher.l_name
        response[teacher.school.name].append(name)

    return (JsonResponse(response))


@csrf_exempt
def submit_attendance(request):
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
            "first_submission_today": true
        }
    """
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
        return JsonResponse({"first_submission_today": True})

    # if the teacher has already checked in today
    #   see mobile_tools for sanitation policy
    else:
        tools.deduplicate_entries(request)
        return JsonResponse({"first_submission_today": False})


def get_lat_long(request):
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
    school = School.objects.get(name=request.get("school_name"))
    return JsonResponse(
        {
            "latitude": school.latitude,
            "longitude": school.longitude
        })


@csrf_exempt
def password_correct(request):
    """
    requires:
        {
            # password is confirmation of mobile user; entered_password is the
            # password the user actually entered.
            password:
            entered_password:
            f_name: "Jackson",
            l_name: "Breyer",
            school_name: "Brandeis"
        }

    returns:
        {
            "password_correct": True
        }
    """
    tools = MobileTools()
    body = tools.get_request_body(request)

    school = School.objects.get(name=body["school_name"])
    teacher = (Teacher.objects.get(school=school,
                                   f_name=body["f_name"],
                                   l_name=body["l_name"]))

    match = body["entered_password"] == teacher.password

    return JsonResponse({"password_correct": match})


def teacher_exists(request):
    """
    requires:
        {
            password:
            "f_name": "Jackson",
            "l_name": "Breyer",
            "school_name": "Brandeis"
        }

    returns:
        {
            "teacher_exists": True
        }

    """
    school = School.objects.get(name=request.get("school_name"))

    exists = Teacher.objects.filter(f_name=request.get("f_name"),
                                    l_name=request.get("l_name"),
                                    school=school).exists()

    return JsonResponse({"teacher_exists": exists})
