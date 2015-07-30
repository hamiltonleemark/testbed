# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0002_auto_20150629_0211'),
    ]

    operations = [
        migrations.RenameField(
            model_name='result',
            old_name='contenxt',
            new_name='context',
        ),
        migrations.RenameField(
            model_name='test',
            old_name='key',
            new_name='keys',
        ),
        migrations.RenameField(
            model_name='testsuite',
            old_name='key',
            new_name='keys',
        ),
    ]
