from tabackend.models import Attendance, Teacher, School
from django.utils import timezone
from datetime import timedelta


class MobileTools:

    def is_mobile_user(self, request):
        return request.get("password") == "stayinschool"

    def reporter_submitted_today(self, reporter, teacher):
        """
        ie: did a reporter with this name submit a report for this
            teacher within the last 15 hours?
        """
        yesterday = timezone.now() - timedelta(hours=15)
        return (Attendance.filter(
                teacher=teacher,
                reporter=reporter,
                date__range=(yesterday, timezone.now())
                ).exists())

    def get_all_teachers_num_times_missing(self):
        """
        TODO: only one value per day

        returns:
        all_schools{
            "Brandeis": {
                "Jackson Breyer": 45
            }
        }
        ...where the main dict maps the school's name to an inner dict.
        The inner dict maps each teacher name to the number of times
        that teacher has been reported missing.
        """
        # add all schools
        all_schools = {school.name: {} for school in School.objects.all()}

        # add all teachers to their appropriate school
        for teacher in Teacher.objects.all():
            all_schools[teacher.school.name][teacher.get_full_name()] = 0

        # log absences for each teacher
        for attendance in Attendance.objects.filter(present=False):
            all_schools[attendance.teacher.school.name][attendance.teacher.get_full_name()] += 1

        return all_schools
