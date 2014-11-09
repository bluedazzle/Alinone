# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0008_auto_20141109_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchant',
            name='faillist',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
    ]
