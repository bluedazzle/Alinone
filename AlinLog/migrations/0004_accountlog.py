# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0015_auto_20141121_1131'),
        ('AlinLog', '0003_auto_20141124_1234'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ltype', models.IntegerField(max_length=2)),
                ('content', models.CharField(max_length=100, null=True, blank=True)),
                ('note', models.CharField(max_length=50, null=True, blank=True)),
                ('log_time', models.DateTimeField(auto_now_add=True)),
                ('merchant', models.ForeignKey(blank=True, to='CronOrder.Merchant', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
