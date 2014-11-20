# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AlinLog', '0006_auto_20141127_1442'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeachLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('req_ip', models.CharField(max_length=15)),
                ('req_time', models.DateTimeField(auto_now_add=True)),
                ('req_param', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
