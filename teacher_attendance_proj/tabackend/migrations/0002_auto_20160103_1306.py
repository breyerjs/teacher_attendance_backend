# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tabackend', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='present',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='reporter',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='gender',
        ),
        migrations.AddField(
            model_name='attendance',
            name='near_school',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attendance',
            name='phone_number',
            field=models.IntegerField(default=42),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='school',
            name='latitude',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='school',
            name='longitude',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teacher',
            name='password',
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
    ]
