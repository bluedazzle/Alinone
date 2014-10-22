# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0009_auto_20141018_1041'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant',
            name='address',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='merchant',
            name='balance',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='merchant',
            name='deadtime',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='merchant',
            name='purchase_type',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='merchant',
            name='recent_days',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sender',
            name='nick',
            field=models.CharField(default=b'sender', max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
    ]
