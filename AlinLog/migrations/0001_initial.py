# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CronLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ltype', models.IntegerField(max_length=2)),
                ('content', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=True)),
                ('log_time', models.DateTimeField(auto_now_add=True, max_length=30)),
                ('err_message', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
