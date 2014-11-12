# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0010_auto_20141111_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant',
            name='netspider_time',
            field=models.DateTimeField(max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
    ]
