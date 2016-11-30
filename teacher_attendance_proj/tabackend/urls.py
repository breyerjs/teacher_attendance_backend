from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^report$', views.report, name='report'),
    url(r'^login$', views.login, name='login'),
    url(r'^submit_attendance$', views.submit_attendance, name='submit_attendance'),
    url(r'^create_teacher$', views.create_teacher, name='create_teacher'),    
]
