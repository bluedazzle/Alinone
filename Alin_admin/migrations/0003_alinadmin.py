# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Alin_admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlinAdmin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_date', models.DateTimeField(auto_created=True)),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=40)),
                ('last_login_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
