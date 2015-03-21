# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AlinLog', '0009_auto_20150303_1709'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProRunTimeLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('error_file', models.CharField(max_length=50)),
                ('error_line', models.IntegerField(max_length=10)),
                ('log_time', models.DateTimeField(auto_now_add=True)),
                ('origin_message', models.TextField(max_length=1000)),
                ('err_message', models.TextField(max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
