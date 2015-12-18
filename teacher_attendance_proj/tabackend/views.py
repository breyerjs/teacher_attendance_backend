from django.shortcuts import render
from django.http import HttpResponse
from .models import School, Teacher, Attendance
from django.http import JsonResponse

"""
TODO:
    1. Generate report for repot view.
    2. Authentication for mobile requests
"""


# WEB API
def report(request):
    return HttpResponse("Hello, world. You're at the Teacher Attendance Report page")


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
