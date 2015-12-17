# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date', models.DateTimeField(verbose_name='date')),
                ('present', models.BooleanField()),
                ('reporter', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=150)),
                ('city', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('f_name', models.CharField(max_length=150)),
                ('l_name', models.CharField(max_length=150)),
                ('gender', models.CharField(max_length=1)),
                ('school', models.ForeignKey(to='tabackend.School')),
            ],
        ),
        migrations.AddField(
            model_name='attendance',
            name='teacher',
            field=models.ForeignKey(to='tabackend.Teacher'),
        ),
    ]
