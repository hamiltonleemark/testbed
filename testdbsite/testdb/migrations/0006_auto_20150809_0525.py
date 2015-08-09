# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0005_testsuiteresult'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testresult',
            name='context',
            field=models.ForeignKey(related_name='test_context', default=None, blank=True, to='testdb.Key', null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='key',
            field=models.ForeignKey(related_name='test_key', default=None, blank=True, to='testdb.Key', null=True),
        ),
    ]
