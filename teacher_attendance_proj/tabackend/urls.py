from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^report$', views.report, name='report'),
    url(r'^get_all_teachers_in_school$', views.get_all_teachers_in_school, name='get_all_teachers_in_school'),
    url(r'^get_all_schools$', views.get_all_schools, name='get_all_schools'),
    url(r'^submit_attendance$', views.submit_attendance, name='submit_attendance'),
]