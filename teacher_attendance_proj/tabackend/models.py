from django.db import models


class School(models.Model):
    # should be unique on name
    name = models.CharField(max_length=150)
    city = models.CharField(max_length=150)

    # for maps
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Teacher(models.Model):
    # should be unique on (f_name, l_name, school)
    f_name = models.CharField(max_length=150)
    l_name = models.CharField(max_length=150)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    password = models.CharField(max_length=150)

    def __str__(self):
        return self.f_name + " " + self.l_name

    def get_full_name(self):
        return self.f_name + " " + self.l_name


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
