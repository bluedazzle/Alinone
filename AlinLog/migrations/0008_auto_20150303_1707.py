# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AlinLog', '0007_seachlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountlog',
            name='content',
            field=models.CharField(max_length=500, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cronlog',
            name='content',
            field=models.CharField(max_length=500),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='runtimelog',
            name='content',
            field=models.CharField(max_length=500),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='seachlog',
            name='req_param',
            field=models.CharField(max_length=500),
            preserve_default=True,
        ),
    ]
