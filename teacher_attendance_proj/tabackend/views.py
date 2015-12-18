from django.shortcuts import render
from django.http import HttpResponse
from .models import School, Teacher, Attendance
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
    attendance = Attendance.objects.all()
    template = loader.get_template('tabackend/report.html')
    context = RequestContext(request, {'attendance': attendance})
    return HttpResponse(template.render(context))

# ===================================================== #
# MOBILE API


def get_all_schools(request):
    """
    returns:
        {
            "schools": [list of school names],
            "password":
        }
    """
    # check this is a mobile user
    tools = MobileTools()
    if not tools.is_mobile_user(request):
        return

    response = {"schools": [school.name for school in School.objects.all()]}
    return (JsonResponse(response))


def get_all_teachers_in_school(request):
    """
    Requires:
        {
            "school_name": "Brandeis",
            "password":
        }

    Returns:
        {
            names: [list of teachers (f_name + " " + l_name)]
            genders[list of genders]
        }

    """
    # check this is a mobile user
    tools = MobileTools()
    if not tools.is_mobile_user(request):
        return

    school_name = request.get("school_name")
    school = School.objects.get(name=school_name)

    names, genders = []
    for teacher in Teacher.objects.filter(school=school):
        names.append(teacher.f_name + " " + teacher.l_name)
        genders.append(teacher.gender)

    response = {
        "names": names,
        "genders": genders
    }
    return (JsonResponse(response))


def submit_attendance(request):
    """
    Requires:
        {
            "f_name": "Jackson",
            "l_name": "Breyer",
            "school_name": "Brandeis",
            "reporter": "Rachelle",
            "present": false,
            "password":
        }

    Returns:
        {
            "submitted": true
        }
    """
    # check this is a mobile user
    tools = MobileTools()
    if not tools.is_mobile_user(request):
        return

    reporter = request.get("reporter")
    teacher = Teacher.objects.get(f_name=request.get("f_name"),
                                  l_name=request.get("l_name"),
                                  school__name=request.get("school_name")
                                  )

    # create + save the new Attendance object, if reporter hasn't reported today
    if not tools.reporter_submitted_today(reporter, teacher):
        Attendance.objects.create(
            date=timezone.now(),
            present=request.get("present"),
            teacher=teacher,
            reporter=reporter
        )

    # send the confirmed response
    return JsonResponse({"submitted": True})
