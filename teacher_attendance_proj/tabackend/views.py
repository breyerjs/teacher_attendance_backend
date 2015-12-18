from django.shortcuts import render
from django.http import HttpResponse
from .models import School, Teacher, Attendance
from django.http import JsonResponse
from django.template import RequestContext, loader
from django.utils import timezone

"""
TODO:
    1. Generate report for repot view.
    2. Authentication for mobile requests
"""


# WEB API
def report(request):
    attendance = Attendance.objects.all()
    template = loader.get_template('tabackend/report.html')
    context = RequestContext(request, {'attendance': attendance})
    return HttpResponse(template.render(context))


# MOBILE API
def get_all_schools(request):
    """
    returns:
        {
            "schools": [list of school names]
        }
    """
    # make this a json output
    response = {"schools": [school.name for school in School.objects.all()]}
    return (JsonResponse(response))


def get_all_teachers_in_school(request):
    """
    Requires:
        {
            "school_name": "Brandeis"
        }

    Returns:
        {
            names: [list of teachers (f_name + " " + l_name)]
        }

    """
    school_name = request.get("name")
    school = School.objects.get(name=school_name)
    # make this a json output
    response = ([teacher.f_name + " " + teacher.l_name
                for teacher in Teacher.objects.filter(school=school)])
    return (JsonResponse(response))


def submit_attendance(request):
    """
    Requires:
        {
            "f_name": "Jackson",
            "l_name": "Breyer",
            "school_name": "Brandeis",
            "reporter": "Rachelle",
            "present": false
        }

    Returns:
        {
            "submitted": true
        }
    """
    teacher = Teacher.objects.get(f_name=request.get("f_name"),
                                  l_name=request.get("l_name"),
                                  school__name=request.get("school_name")
                                  )

    # create + save the new Attendance object
    Attendance.objects.create(
        date=timezone.now(),
        present=request.get("present"),
        teacher=teacher,
        reporter=request.get("reporter")
    )

    # send the confirmed response
    return JsonResponse({"submitted": True})
