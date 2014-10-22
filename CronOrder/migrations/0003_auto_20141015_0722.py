# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0002_auto_20141015_0720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayorder',
            name='merchant',
            field=models.ForeignKey(blank=True, to='CronOrder.Merchant', null=True),
        ),
    ]
