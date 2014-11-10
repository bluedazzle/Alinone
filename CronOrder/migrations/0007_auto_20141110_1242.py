# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0006_auto_20141109_1722'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tdish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dish_name', models.CharField(max_length=30)),
                ('dish_price', models.FloatField(max_length=5)),
                ('dish_count', models.IntegerField(max_length=5)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TotalOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_id_alin', models.CharField(unique=True, max_length=22)),
                ('order_id_old', models.CharField(max_length=20)),
                ('order_time', models.DateTimeField(max_length=30)),
                ('send_time', models.DateTimeField(max_length=30)),
                ('phone', models.CharField(max_length=13)),
                ('pay', models.BooleanField(default=False)),
                ('address', models.CharField(max_length=50)),
                ('platform', models.IntegerField(max_length=1)),
                ('origin_price', models.FloatField(max_length=10)),
                ('note', models.CharField(max_length=100, null=True, blank=True)),
                ('promotion', models.CharField(max_length=50, null=True, blank=True)),
                ('real_price', models.FloatField(max_length=10)),
                ('status', models.IntegerField(max_length=1)),
                ('finish_by', models.CharField(max_length=20, null=True, blank=True)),
                ('qr_path', models.CharField(max_length=20, null=True, blank=True)),
                ('bind_sender', models.ForeignKey(blank=True, to='CronOrder.Sender', null=True)),
                ('merchant', models.ForeignKey(blank=True, to='CronOrder.Merchant', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tdish',
            name='order',
            field=models.ForeignKey(blank=True, to='CronOrder.TotalOrder', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='merchant',
            name='faillist',
            field=models.CharField(max_length=1000, null=True, blank=True),
            preserve_default=True,
        ),
    ]
