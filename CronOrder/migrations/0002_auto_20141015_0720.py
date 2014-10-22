# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='order',
            field=models.ForeignKey(blank=True, to='CronOrder.DayOrder', null=True),
        ),
    ]
