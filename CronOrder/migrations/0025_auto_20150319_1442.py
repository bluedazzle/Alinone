# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0024_auto_20150319_1424'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dayorder',
            name='finish_by',
        ),
        migrations.RemoveField(
            model_name='totalorder',
            name='finish_by',
        ),
        migrations.AddField(
            model_name='dayorder',
            name='finished_by',
            field=models.ForeignKey(related_name='forders', blank=True, to='CronOrder.Sender', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='totalorder',
            name='finished_by',
            field=models.ForeignKey(related_name='tforders', blank=True, to='CronOrder.Sender', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dayorder',
            name='bind_sender',
            field=models.ForeignKey(related_name='orders', blank=True, to='CronOrder.Sender', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='totalorder',
            name='bind_sender',
            field=models.ForeignKey(related_name='torders', blank=True, to='CronOrder.Sender', null=True),
            preserve_default=True,
        ),
    ]
