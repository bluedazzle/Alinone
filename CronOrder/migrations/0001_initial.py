# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='abc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('usrid', models.IntegerField(default=1)),
                ('i', models.IntegerField(default=1)),
                ('ison', models.IntegerField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DayOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_id_alin', models.CharField(unique=True, max_length=20)),
                ('order_id_old', models.CharField(max_length=20)),
                ('order_time', models.DateTimeField(max_length=30)),
                ('send_time', models.DateTimeField(max_length=30)),
                ('phone', models.CharField(max_length=13)),
                ('address', models.CharField(max_length=50)),
                ('platform', models.IntegerField(max_length=1)),
                ('origin_price', models.FloatField(max_length=10)),
                ('promotion', models.CharField(max_length=50)),
                ('real_price', models.FloatField(max_length=10)),
                ('status', models.IntegerField(max_length=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dish_name', models.CharField(max_length=30)),
                ('dish_price', models.FloatField(max_length=5)),
                ('dish_count', models.IntegerField(max_length=5)),
                ('order', models.ForeignKey(to='CronOrder.DayOrder', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('name', models.CharField(max_length=50)),
                ('alin_account', models.CharField(unique=True, max_length=15)),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('tao_account', models.CharField(max_length=15, blank=True)),
                ('tao_passwd', models.CharField(max_length=50, blank=True)),
                ('mei_account', models.CharField(max_length=15, blank=True)),
                ('mei_passwd', models.CharField(max_length=50, blank=True)),
                ('ele_account', models.CharField(max_length=15, blank=True)),
                ('ele_passwd', models.CharField(max_length=50, blank=True)),
                ('is_online', models.BooleanField(default=True)),
                ('is_open', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sender',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.CharField(unique=True, max_length=15)),
                ('passwd', models.CharField(max_length=50)),
                ('lng', models.FloatField(max_length=10, null=True, blank=True)),
                ('lat', models.FloatField(max_length=10, null=True, blank=True)),
                ('update_time', models.DateTimeField(max_length=30, null=True, blank=True)),
                ('bind_order', models.ManyToManyField(to='CronOrder.DayOrder', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='dayorder',
            name='merchant',
            field=models.ForeignKey(default=b'0', to='CronOrder.Merchant'),
            preserve_default=True,
        ),
    ]
