# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0008_dayorder_finish_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='sender',
            name='active_time',
            field=models.DateTimeField(max_length=30, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dayorder',
            name='bind_sender',
            field=models.ForeignKey(related_name=b'order', blank=True, to='CronOrder.Sender', null=True),
        ),
    ]
