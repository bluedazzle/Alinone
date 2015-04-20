# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Alin_admin', '0002_auto_20150420_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alinadmin',
            name='last_login_date',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
