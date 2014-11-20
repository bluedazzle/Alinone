# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0013_auto_20141121_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchant',
            name='todaynum',
            field=models.IntegerField(default=1),
        ),
    ]
