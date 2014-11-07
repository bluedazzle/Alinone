# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DayOrder',
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
                ('promotion', models.CharField(max_length=50)),
                ('real_price', models.FloatField(max_length=10)),
                ('status', models.IntegerField(max_length=1)),
                ('finish_by', models.CharField(max_length=20, null=True, blank=True)),
                ('qr_path', models.CharField(max_length=20, null=True, blank=True)),
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
                ('order', models.ForeignKey(blank=True, to='CronOrder.DayOrder', null=True)),
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
                ('address', models.CharField(max_length=100, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('tao_account', models.CharField(max_length=100, blank=True)),
                ('tao_passwd', models.CharField(max_length=50, blank=True)),
                ('mei_account', models.CharField(max_length=100, blank=True)),
                ('mei_passwd', models.CharField(max_length=50, blank=True)),
                ('ele_account', models.CharField(max_length=100, blank=True)),
                ('ele_passwd', models.CharField(max_length=50, blank=True)),
                ('reg_time', models.DateTimeField(null=True, blank=True)),
                ('bind_pic', models.CharField(max_length=30, null=True, blank=True)),
                ('is_online', models.BooleanField(default=True)),
                ('is_open', models.BooleanField(default=False)),
                ('todaynum', models.IntegerField(default=0)),
                ('purchase_type', models.IntegerField(default=0)),
                ('deadtime', models.DateTimeField(null=True, blank=True)),
                ('recent_days', models.IntegerField(null=True, blank=True)),
                ('balance', models.FloatField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='dayorder',
            name='merchant',
            field=models.ForeignKey(blank=True, to='CronOrder.Merchant', null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Sender',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.CharField(unique=True, max_length=15)),
                ('nick', models.CharField(default=b'sender', max_length=20, null=True, blank=True)),
                ('passwd', models.CharField(max_length=50)),
                ('lng', models.FloatField(max_length=10, null=True, blank=True)),
                ('lat', models.FloatField(max_length=10, null=True, blank=True)),
                ('update_time', models.DateTimeField(max_length=30, null=True, blank=True)),
                ('private_token', models.CharField(max_length=32, unique=True, null=True, blank=True)),
                ('active_time', models.DateTimeField(max_length=30, null=True, blank=True)),
                ('verify_code', models.CharField(max_length=6, null=True, blank=True)),
                ('is_verify', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='merchant',
            name='bind_sender',
            field=models.ManyToManyField(to='CronOrder.Sender', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dayorder',
            name='bind_sender',
            field=models.ForeignKey(blank=True, to='CronOrder.Sender', null=True),
            preserve_default=True,
        ),
    ]
