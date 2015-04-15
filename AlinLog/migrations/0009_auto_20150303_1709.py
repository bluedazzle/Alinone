# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AlinLog', '0008_auto_20150303_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='runtimelog',
            name='err_message',
            field=models.CharField(max_length=500, null=True, blank=True),
            preserve_default=True,
        ),
    ]
