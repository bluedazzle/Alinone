# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0003_auto_20141015_0722'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant',
            name='todaynum',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
