# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AlinLog', '0010_proruntimelog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proruntimelog',
            name='error_file',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
    ]
