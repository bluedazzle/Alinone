# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0008_merchant_update_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant',
            name='auto_print',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='merchant',
            name='update_time',
            field=models.DateField(max_length=20, null=True, blank=True),
        ),
    ]
