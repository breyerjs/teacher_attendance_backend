# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-01-03 00:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabackend', '0007_auto_20161209_0727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='name',
            field=models.CharField(max_length=150),
        ),
    ]
