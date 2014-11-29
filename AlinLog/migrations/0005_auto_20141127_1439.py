# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AlinLog', '0004_accountlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountlog',
            name='account',
            field=models.CharField(max_length=40, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='accountlog',
            name='atype',
            field=models.IntegerField(default=0, max_length=2),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='accountlog',
            name='merchant',
        ),
        migrations.AlterField(
            model_name='accountlog',
            name='ltype',
            field=models.IntegerField(default=0, max_length=2),
        ),
    ]
