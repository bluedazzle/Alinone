# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0006_auto_20141017_0524'),
    ]

    operations = [
        migrations.AddField(
            model_name='sender',
            name='private_token',
            field=models.CharField(max_length=32, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
    ]
