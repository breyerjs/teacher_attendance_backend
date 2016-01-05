from django.shortcuts import render
from django.http import HttpResponse
from tabackend.models import School, Teacher, Attendance
from django.http import JsonResponse
from django.template import RequestContext, loader
from django.utils import timezone
from .mobile_tools import MobileTools

"""
TODO:
    1. Generate report for report view.
"""

# ===================================================== #
# WEB API


def report(request):
    """
    TODO
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
    # for testing only!!
    return JsonResponse({"data": request.body})

    # check this is a mobile user
    tools = MobileTools()
    if not tools.is_mobile_user(request):
        return

    response = {school.name: [] for school in School.objects.all()}
    for teacher in Teacher.objects.all():
        name = teacher.f_name + " " + teacher.l_name
        response[teacher.school.name].append(name)

    return (JsonResponse(response))


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
    # check this is a mobile user
    tools = MobileTools()
    if not tools.is_mobile_user(request):
        return

    teacher = Teacher.objects.get(f_name=request.get("f_name"),
                                  l_name=request.get("l_name"),
                                  school__name=request.get("school_name")
                                  )

    # create + save the new Attendance object, if reporter hasn't reported today

    if not tools.teacher_submitted_today(teacher):
        Attendance.objects.create(
            date=timezone.now(),
            near_school=request.get("near_school"),
            teacher=teacher,
            phone_number=request.get("phone_number")
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

    # check this is a mobile user
    tools = MobileTools()
    if not tools.is_mobile_user(request):
        return

    school = School.objects.get(name=request.get("school_name"))
    return JsonResponse(
        {
            "latitude": school.latitude,
            "longitude": school.longitude
        })


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
    # check this is a mobile user
    tools = MobileTools()
    if not tools.is_mobile_user(request):
        return

    school = School.get(name=request.get("school_name"))
    teacher = Teacher.filter(school=school,
                             f_name=request.get("f_name"),
                             l_name=request.get("l_name"))

    match = request.get("entered_password") == teacher.password

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
    # check this is a mobile user
    tools = MobileTools()
    if not tools.is_mobile_user(request):
        return

    school = School.objects.get(name=request.get("school_name"))

    exists = Teacher.objects.filter(f_name=request.get("f_name"),
                                    l_name=request.get("l_name"),
                                    school=school).exists()

    return JsonResponse({"teacher_exists": exists})
