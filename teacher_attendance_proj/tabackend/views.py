from django.http import HttpResponse, JsonResponse
from django.template import RequestContext, loader
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

"""
{
    "username": "jbreyer",
    "password": "guest"
}
"""
def login(request):
    request_body = get_request_body(request)
    username = request_body.get('username')
    password = request_body.get('password')
    if not Logic.teacher_credentials_valid(username, password):
        return HttpResponse(status=403)
    return HttpResponse(status=204)


"""
    {
        "username": "jbreyer"
        "password": "guest",
        "latitude": number,
        "longitude": number,
        "phone_number": 2025551234,
    }
"""
def submit_attendance(request):
    if request.method != 'POST':
        return HttpResponse(status=405)
    Logic().submit_attendance(get_request_body(request))
    return HttpResponse(status=204)


# ===================================================== #
# HELPER METHODS

# Assumes each element from the request body is non null and loaded 
# into model via request_body.get('keyName')
def request_is_valid(model):
    for key in model:
        if model.get(key) is None:
            return False
    return True

def get_request_body(request):
    body_unicode = request.body.decode('utf-8')
    return json.loads(body_unicode)
