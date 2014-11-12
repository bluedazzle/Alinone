# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0005_auto_20141108_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='dayorder',
            name='note',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='merchant',
            name='ele_status',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='merchant',
            name='mei_status',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='merchant',
            name='tao_refreshkey',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='merchant',
            name='tao_sessionkey',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='merchant',
            name='tao_shopid',
            field=models.CharField(max_length=30, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='merchant',
            name='tao_status',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dayorder',
            name='promotion',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
