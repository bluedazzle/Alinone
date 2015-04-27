# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0001_initial'),
        ('merchant_page', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedBack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('merchant', models.ForeignKey(related_name='feedback', to='CronOrder.Merchant')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
