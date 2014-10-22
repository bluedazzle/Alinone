# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0004_merchant_todaynum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayorder',
            name='order_id_alin',
            field=models.CharField(unique=True, max_length=22),
        ),
    ]
