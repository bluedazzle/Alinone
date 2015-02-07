# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CronOrder', '0019_catchedata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catchedata',
            name='ele_cookie',
            field=models.TextField(max_length=5000, null=True, blank=True),
        ),
    ]
