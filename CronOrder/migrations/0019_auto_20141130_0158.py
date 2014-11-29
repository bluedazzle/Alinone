# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0018_auto_20141203_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayorder',
            name='bind_sender',
            field=models.ForeignKey(related_name='order', blank=True, to='CronOrder.Sender', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dish',
            name='order',
            field=models.ForeignKey(related_name='dishs', blank=True, to='CronOrder.DayOrder', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='merchant',
            name='bind_sender',
            field=models.ManyToManyField(related_name='sender', null=True, to='CronOrder.Sender', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tdish',
            name='order',
            field=models.ForeignKey(related_name='tdishs', blank=True, to='CronOrder.TotalOrder', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='totalorder',
            name='bind_sender',
            field=models.ForeignKey(related_name='torder', blank=True, to='CronOrder.Sender', null=True),
            preserve_default=True,
        ),
    ]
