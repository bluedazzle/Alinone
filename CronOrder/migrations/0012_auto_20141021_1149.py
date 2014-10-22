# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0011_dayorder_pay'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='order',
            field=models.ForeignKey(related_name=b'dishs', blank=True, to='CronOrder.DayOrder', null=True),
        ),
    ]
