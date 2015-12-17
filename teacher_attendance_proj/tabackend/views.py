from django.shortcuts import render
from django.http import HttpResponse


def report(request):
    return HttpResponse("Hello, world. You're at the Teacher Attendance Report page")
