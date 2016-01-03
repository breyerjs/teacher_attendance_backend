from tabackend.models import Attendance, Teacher, School
from django.utils import timezone
from datetime import timedelta


class MobileTools:

    def is_mobile_user(self, request):
        return request.get("password") == "stayinschool"

    def teacher_submitted_today(self, teacher):
        """
        ie: did this teacher check in within the last 15 hours?
        """
        yesterday = timezone.now() - timedelta(hours=15)
        return (Attendance.filter(
                teacher=teacher,
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
        for attendance in Attendance.objects.filter(near_school=False):
            all_schools[attendance.teacher.school.name][attendance.teacher.get_full_name()] += 1

        return all_schools


def deduplicate_entries(request):
    """
    requires a request with dict from submit_attendance
    only saves if:
        a) this has near_school=True
        b) there is no near_school=True for this teacher

    in that case, deletes the near_school=False entry
    """

    teacher = Teacher.objects.get(f_name=request.get("f_name"),
                                  l_name=request.get("l_name"),
                                  school__name=request.get("school_name")
                                  )

    # get Attendance for this teacher for the past day
    # currently unifinished!
