# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0004_auto_20141108_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant',
            name='ele_message',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='merchant',
            name='mei_message',
            field=models.CharField(default=datetime.date(2014, 11, 8), max_length=100, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='merchant',
            name='tao_message',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='merchant',
            name='mei_passwd',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
    ]
