# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AlinLog', '0002_runtimelog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='runtimelog',
            name='merchant',
            field=models.ForeignKey(blank=True, to='CronOrder.Merchant', null=True),
        ),
    ]
