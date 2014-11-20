# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0015_auto_20141121_1131'),
        ('AlinLog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RunTimeLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ltype', models.IntegerField(max_length=2)),
                ('content', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=True)),
                ('log_time', models.DateTimeField(auto_now_add=True)),
                ('err_message', models.CharField(max_length=100, null=True, blank=True)),
                ('merchant', models.ForeignKey(to='CronOrder.Merchant')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
