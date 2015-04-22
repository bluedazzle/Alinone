# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CatcheData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ele_cookie', models.TextField(max_length=5000, null=True, blank=True)),
                ('mei_token', models.CharField(max_length=128, null=True, blank=True)),
                ('mei_id', models.CharField(max_length=20, null=True, blank=True)),
                ('mei_acctid', models.CharField(max_length=20, null=True, blank=True)),
                ('mei_lastorderid', models.CharField(max_length=20, null=True, blank=True)),
                ('mei_sid', models.CharField(max_length=128, null=True, blank=True)),
                ('mei_verify', models.CharField(max_length=10, null=True, blank=True)),
                ('mei_need_verify', models.BooleanField(default=False)),
                ('tdd_sessionid', models.CharField(max_length=500, null=True, blank=True)),
                ('tdd_shopid', models.CharField(max_length=20, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DayOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_id_alin', models.CharField(unique=True, max_length=22)),
                ('order_id_old', models.CharField(max_length=30)),
                ('order_time', models.DateTimeField(max_length=30)),
                ('send_time', models.DateTimeField(max_length=30)),
                ('phone', models.CharField(max_length=52)),
                ('pay', models.BooleanField(default=False)),
                ('address', models.CharField(max_length=50)),
                ('platform', models.IntegerField(max_length=1)),
                ('origin_price', models.FloatField(max_length=10)),
                ('note', models.CharField(max_length=100, null=True, blank=True)),
                ('promotion', models.CharField(max_length=50, null=True, blank=True)),
                ('real_price', models.FloatField(max_length=10)),
                ('status', models.IntegerField(max_length=1)),
                ('qr_path', models.CharField(max_length=50, null=True, blank=True)),
                ('plat_num', models.CharField(max_length=10, null=True, blank=True)),
                ('day_num', models.CharField(max_length=10, null=True, blank=True)),
            ],
            options={
                'abstract': False,
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
                ('order', models.ForeignKey(related_name='dishs', blank=True, to='CronOrder.DayOrder', null=True)),
            ],
            options={
                'abstract': False,
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
                ('tao_passwd', models.CharField(max_length=500, blank=True)),
                ('tao_sessionkey', models.CharField(max_length=100, null=True, blank=True)),
                ('tao_refreshkey', models.CharField(max_length=100, null=True, blank=True)),
                ('tao_shopid', models.CharField(max_length=30, null=True, blank=True)),
                ('tao_message', models.CharField(max_length=100, null=True, blank=True)),
                ('tao_status', models.BooleanField(default=False)),
                ('mei_account', models.CharField(max_length=100, blank=True)),
                ('mei_passwd', models.CharField(max_length=500, null=True, blank=True)),
                ('mei_message', models.CharField(max_length=100, blank=True)),
                ('mei_status', models.BooleanField(default=False)),
                ('ele_account', models.CharField(max_length=100, blank=True)),
                ('ele_passwd', models.CharField(max_length=500, blank=True)),
                ('ele_message', models.CharField(max_length=100, null=True, blank=True)),
                ('ele_status', models.BooleanField(default=False)),
                ('reg_time', models.DateTimeField(null=True, blank=True)),
                ('bind_pic', models.CharField(max_length=30, null=True, blank=True)),
                ('faillist', models.CharField(max_length=1000, null=True, blank=True)),
                ('update_time', models.DateTimeField(max_length=20, null=True, blank=True)),
                ('netspider_time', models.DateTimeField(max_length=20, null=True, blank=True)),
                ('auto_print', models.BooleanField(default=True)),
                ('is_online', models.BooleanField(default=True)),
                ('is_open', models.BooleanField(default=False)),
                ('todaynum', models.IntegerField(default=1)),
                ('purchase_type', models.IntegerField(default=0)),
                ('deadtime', models.DateTimeField(null=True, blank=True)),
                ('recent_days', models.IntegerField(null=True, blank=True)),
                ('balance', models.FloatField(null=True, blank=True)),
                ('verify', models.BooleanField(default=False)),
                ('belong', models.CharField(default=b'11', max_length=10)),
                ('private_token', models.CharField(max_length=64, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sender',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('phone', models.CharField(unique=True, max_length=15)),
                ('nick', models.CharField(default=b'sender', max_length=20, null=True, blank=True)),
                ('lng', models.FloatField(max_length=10, null=True, blank=True)),
                ('lat', models.FloatField(max_length=10, null=True, blank=True)),
                ('update_time', models.DateTimeField(max_length=30, null=True, blank=True)),
                ('private_token', models.CharField(max_length=32, unique=True, null=True, blank=True)),
                ('active_time', models.DateTimeField(max_length=30, null=True, blank=True)),
                ('verify_code', models.CharField(max_length=6, null=True, blank=True)),
                ('is_verify', models.BooleanField(default=False)),
                ('status', models.CharField(default=b'', max_length=10, null=True, blank=True)),
                ('today_sends', models.IntegerField(default=0, max_length=5, null=True, blank=True)),
                ('offline_num', models.IntegerField(default=0, max_length=5, null=True, blank=True)),
                ('online_num', models.IntegerField(default=0, max_length=5, null=True, blank=True)),
                ('offline_money', models.FloatField(default=0, max_length=10, null=True, blank=True)),
                ('online_money', models.FloatField(default=0, max_length=10, null=True, blank=True)),
                ('belong', models.CharField(default=b'11', max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tdish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dish_name', models.CharField(max_length=30)),
                ('dish_price', models.FloatField(max_length=5)),
                ('dish_count', models.IntegerField(max_length=5)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TotalOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_id_alin', models.CharField(unique=True, max_length=22)),
                ('order_id_old', models.CharField(max_length=30)),
                ('order_time', models.DateTimeField(max_length=30)),
                ('send_time', models.DateTimeField(max_length=30)),
                ('phone', models.CharField(max_length=52)),
                ('pay', models.BooleanField(default=False)),
                ('address', models.CharField(max_length=50)),
                ('platform', models.IntegerField(max_length=1)),
                ('origin_price', models.FloatField(max_length=10)),
                ('note', models.CharField(max_length=100, null=True, blank=True)),
                ('promotion', models.CharField(max_length=50, null=True, blank=True)),
                ('real_price', models.FloatField(max_length=10)),
                ('status', models.IntegerField(max_length=1)),
                ('qr_path', models.CharField(max_length=50, null=True, blank=True)),
                ('day_num', models.CharField(max_length=10, null=True, blank=True)),
                ('bind_sender', models.ForeignKey(related_name='torders', blank=True, to='CronOrder.Sender', null=True)),
                ('finished_by', models.ForeignKey(related_name='tforders', blank=True, to='CronOrder.Sender', null=True)),
                ('merchant', models.ForeignKey(blank=True, to='CronOrder.Merchant', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tdish',
            name='order',
            field=models.ForeignKey(related_name='tdishs', blank=True, to='CronOrder.TotalOrder', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='merchant',
            name='bind_sender',
            field=models.ManyToManyField(related_name='sender', null=True, to='CronOrder.Sender', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dayorder',
            name='bind_sender',
            field=models.ForeignKey(related_name='orders', blank=True, to='CronOrder.Sender', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dayorder',
            name='finished_by',
            field=models.ForeignKey(related_name='forders', blank=True, to='CronOrder.Sender', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dayorder',
            name='merchant',
            field=models.ForeignKey(blank=True, to='CronOrder.Merchant', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='catchedata',
            name='merchant',
            field=models.OneToOneField(related_name='Cache', to='CronOrder.Merchant'),
            preserve_default=True,
        ),
    ]
