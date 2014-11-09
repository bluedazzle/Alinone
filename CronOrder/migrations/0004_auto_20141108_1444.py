# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0003_remove_sender_passwd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchant',
            name='ele_passwd',
            field=models.CharField(max_length=500, blank=True),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='mei_passwd',
            field=models.CharField(max_length=500, blank=True),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='tao_passwd',
            field=models.CharField(max_length=500, blank=True),
        ),
    ]
