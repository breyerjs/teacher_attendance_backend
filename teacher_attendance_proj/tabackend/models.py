from django.db import models
from django.contrib.auth.models import User


class School(models.Model):
    # should be unique on name
    name = models.CharField(max_length=150, primary_key=True)
    city = models.CharField(max_length=150)

    # for maps
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'city')

class Teacher(User):
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + " " + self.last_name



class Attendance(models.Model):
    date = models.DateTimeField('date')
    near_school = models.BooleanField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    phone_number = models.IntegerField()

    def __str__(self):
        if self.near_school:
            here = "near school"
        else:
            here = "not near school"

        return (str(self.date) + " " + self.teacher.l_name + " was " +
                here + ".")
