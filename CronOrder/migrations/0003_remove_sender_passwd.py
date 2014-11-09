# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0002_auto_20141107_1043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sender',
            name='passwd',
        ),
    ]
