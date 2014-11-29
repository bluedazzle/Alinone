# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ProxyWork', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proxy',
            name='req_times',
            field=models.IntegerField(default=0, max_length=2),
            preserve_default=True,
        ),
    ]
