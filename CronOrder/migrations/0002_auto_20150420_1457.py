# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant',
            name='belongs',
            field=models.CharField(default=b'11', max_length=10),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sender',
            name='belongs',
            field=models.CharField(default=b'11', max_length=10),
            preserve_default=True,
        ),
    ]
