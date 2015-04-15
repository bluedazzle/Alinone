# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0017_auto_20141130_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='sender',
            name='offline_money',
            field=models.FloatField(default=0, max_length=10, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sender',
            name='offline_num',
            field=models.IntegerField(default=0, max_length=5, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sender',
            name='online_money',
            field=models.FloatField(default=0, max_length=10, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sender',
            name='online_num',
            field=models.IntegerField(default=0, max_length=5, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sender',
            name='status',
            field=models.CharField(default=b'', max_length=10, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sender',
            name='today_sends',
            field=models.IntegerField(default=0, max_length=5, null=True, blank=True),
            preserve_default=True,
        ),
    ]
