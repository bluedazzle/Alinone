# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0015_auto_20141121_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='dayorder',
            name='plat_num',
            field=models.IntegerField(max_length=5, null=True, blank=True),
            preserve_default=True,
        ),
    ]
