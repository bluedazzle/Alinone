# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0009_auto_20141110_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchant',
            name='update_time',
            field=models.DateTimeField(max_length=20, null=True, blank=True),
        ),
    ]
