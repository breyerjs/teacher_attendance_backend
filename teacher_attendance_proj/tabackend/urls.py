from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^report$', views.report, name='report'),
    url(r'^get_all_schools_and_teachers$', views.get_all_schools_and_teachers, name='get_all_schools_and_teachers'),
    url(r'^submit_attendance$', views.submit_attendance, name='submit_attendance'),
    url(r'^get_lat_long$', views.get_lat_long, name='get_lat_long'),
    url(r'^create_user$', views.create_user, name='create_user'),   
    url(r'^create_teacher$', views.create_teacher, name='create_teacher'),    

]
