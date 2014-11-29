# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AlinLog', '0005_auto_20141127_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountlog',
            name='atype',
            field=models.CharField(default=b'0', max_length=5),
        ),
    ]
