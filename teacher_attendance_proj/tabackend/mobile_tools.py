from .models import Attendance, Teacher, School
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
