# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0014_auto_20141121_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayorder',
            name='order_id_old',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='dayorder',
            name='phone',
            field=models.CharField(max_length=52),
        ),
        migrations.AlterField(
            model_name='totalorder',
            name='order_id_old',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='totalorder',
            name='phone',
            field=models.CharField(max_length=52),
        ),
    ]
