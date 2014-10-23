# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0012_auto_20141021_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='sender',
            name='is_verify',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sender',
            name='verify_code',
            field=models.CharField(max_length=6, null=True, blank=True),
            preserve_default=True,
        ),
    ]
