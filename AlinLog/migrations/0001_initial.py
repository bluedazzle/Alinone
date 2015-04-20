# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.CharField(max_length=40, null=True, blank=True)),
                ('atype', models.CharField(default=b'0', max_length=5)),
                ('ltype', models.IntegerField(default=0, max_length=2)),
                ('content', models.CharField(max_length=500, null=True, blank=True)),
                ('note', models.CharField(max_length=50, null=True, blank=True)),
                ('log_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CronLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ltype', models.IntegerField(max_length=2)),
                ('content', models.CharField(max_length=500)),
                ('status', models.BooleanField(default=True)),
                ('log_time', models.DateTimeField(auto_now_add=True, max_length=30)),
                ('err_message', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProRunTimeLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('error_file', models.CharField(max_length=200)),
                ('error_line', models.IntegerField(max_length=10)),
                ('log_time', models.DateTimeField(auto_now_add=True)),
                ('origin_message', models.TextField(max_length=1000)),
                ('err_message', models.TextField(max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RunTimeLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ltype', models.IntegerField(max_length=2)),
                ('content', models.CharField(max_length=500)),
                ('status', models.BooleanField(default=True)),
                ('log_time', models.DateTimeField(auto_now_add=True)),
                ('err_message', models.CharField(max_length=500, null=True, blank=True)),
                ('merchant', models.ForeignKey(blank=True, to='CronOrder.Merchant', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SeachLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('req_ip', models.CharField(max_length=15)),
                ('req_time', models.DateTimeField(auto_now_add=True)),
                ('req_param', models.CharField(max_length=500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
