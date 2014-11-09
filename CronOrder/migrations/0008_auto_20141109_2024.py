# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0007_merchant_faillist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchant',
            name='faillist',
            field=models.CharField(default=b'', max_length=1000),
        ),
    ]
