# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0005_auto_20141016_0731'),
    ]

    operations = [
        migrations.DeleteModel(
            name='abc',
        ),
        migrations.RemoveField(
            model_name='sender',
            name='bind_order',
        ),
        migrations.AddField(
            model_name='dayorder',
            name='bind_sender',
            field=models.ForeignKey(blank=True, to='CronOrder.Sender', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='merchant',
            name='bind_sender',
            field=models.ManyToManyField(related_name=b'sender', null=True, to='CronOrder.Sender', blank=True),
            preserve_default=True,
        ),
    ]
