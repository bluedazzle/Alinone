# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sender',
            name='last_login',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sender',
            name='password',
            field=models.CharField(default=datetime.date(2014, 11, 7), max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
    ]
