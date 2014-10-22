# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0010_auto_20141019_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='dayorder',
            name='pay',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
