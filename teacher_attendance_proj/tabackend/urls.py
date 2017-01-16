from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^report$', views.report, name='report'),
    url(r'^login$', views.login, name='login'),
    url(r'^submit_attendance$', views.submit_attendance, name='submit_attendance'),
]
