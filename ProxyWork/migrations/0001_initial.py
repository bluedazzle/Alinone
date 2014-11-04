# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0016_auto_20141030_1649'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proxy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=30)),
                ('get_time', models.DateTimeField(max_length=30)),
                ('is_used', models.BooleanField(default=False)),
                ('is_online', models.BooleanField(default=False)),
                ('bind_merchant', models.ForeignKey(blank=True, to='CronOrder.Merchant', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
