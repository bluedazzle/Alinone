# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0016_dayorder_plat_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayorder',
            name='plat_num',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
    ]
