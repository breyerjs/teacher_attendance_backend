# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-11-24 23:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabackend', '0004_auto_20161124_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='name',
            field=models.CharField(max_length=150, primary_key=True, serialize=False),
        ),
        migrations.RemoveField(
            model_name='school',
            name='id',
        ),
        migrations.AlterUniqueTogether(
            name='school',
            unique_together=set([('name', 'city')]),
        ),
    ]