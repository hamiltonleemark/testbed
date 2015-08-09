# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0001_squashed_0002_test_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='key',
            name='config_type',
            field=models.IntegerField(default=0, choices=[(0, b'ANY'), (1, b'STRICT')]),
        ),
    ]
