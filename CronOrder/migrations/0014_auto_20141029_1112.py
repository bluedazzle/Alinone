# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0013_auto_20141023_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchant',
            name='ele_account',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='mei_account',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='tao_account',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
