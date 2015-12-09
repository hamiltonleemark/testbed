# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0003_auto_20151208_0721'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='keys',
            new_name='kvps',
        ),
        migrations.RenameField(
            model_name='productkeyset',
            old_name='testkey',
            new_name='kvp',
        ),
        migrations.RenameField(
            model_name='testfile',
            old_name='testsuite',
            new_name='test',
        ),
        migrations.RenameField(
            model_name='testsuite',
            old_name='keys',
            new_name='kvps',
        ),
    ]
