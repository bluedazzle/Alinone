# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0014_auto_20141029_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant',
            name='reg_time',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
