# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0011_merchant_netspider_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayorder',
            name='qr_path',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
