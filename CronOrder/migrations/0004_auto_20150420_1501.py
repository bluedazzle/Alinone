# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0003_auto_20150420_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchant',
            name='belongs',
            field=models.CharField(default=b'11', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sender',
            name='belongs',
            field=models.CharField(default=b'11', max_length=100),
            preserve_default=True,
        ),
    ]
