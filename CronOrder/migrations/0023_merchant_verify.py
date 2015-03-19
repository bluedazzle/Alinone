# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0022_auto_20150303_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant',
            name='verify',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
