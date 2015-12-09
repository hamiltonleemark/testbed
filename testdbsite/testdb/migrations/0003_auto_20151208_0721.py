# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0002_auto_20151208_0717'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testkeyset',
            old_name='testkey',
            new_name='kvp',
        ),
        migrations.RenameField(
            model_name='testsuitekeyset',
            old_name='testkey',
            new_name='kvp',
        ),
    ]
