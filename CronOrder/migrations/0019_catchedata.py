# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0018_auto_20141203_1400'),
    ]

    operations = [
        migrations.CreateModel(
            name='CatcheData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ele_cookie', models.CharField(max_length=5000, null=True, blank=True)),
                ('mei_token', models.CharField(max_length=128, null=True, blank=True)),
                ('mei_id', models.CharField(max_length=20, null=True, blank=True)),
                ('mei_acctid', models.CharField(max_length=20, null=True, blank=True)),
                ('mei_lastorderid', models.CharField(max_length=20, null=True, blank=True)),
                ('mei_sid', models.CharField(max_length=128, null=True, blank=True)),
                ('tdd_sessionid', models.CharField(max_length=500, null=True, blank=True)),
                ('tdd_shopid', models.CharField(max_length=20, null=True, blank=True)),
                ('merchant', models.OneToOneField(to='CronOrder.Merchant')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
