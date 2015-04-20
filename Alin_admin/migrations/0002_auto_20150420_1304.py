# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Alin_admin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alinadmin',
            name='password',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
    ]
