# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0007_auto_20141110_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant',
            name='update_time',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
