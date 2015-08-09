# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0002_key_config_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='name',
        ),
    ]
