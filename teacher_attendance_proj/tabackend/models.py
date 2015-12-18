from django.db import models


class School(models.Model):
    # should be unique on name
    name = models.CharField(max_length=150)
    city = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    # should be unique on (f_name, l_name, school)
    f_name = models.CharField(max_length=150)
    l_name = models.CharField(max_length=150)
    gender = models.CharField(max_length=1)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.f_name + " " + self.l_name


class Attendance(models.Model):
    date = models.DateTimeField('date')
    present = models.BooleanField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    reporter = models.CharField(max_length=200)

    def __str__(self):
        if self.present:
            here = "present"
        else:
            here = "missing"

        return (str(self.date) + " " + self.teacher.l_name + " reported " +
                here + " by " + self.reporter)
