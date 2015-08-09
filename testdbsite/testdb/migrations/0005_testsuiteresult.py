# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0004_auto_20150809_0502'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestsuiteResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.DecimalField(max_digits=24, decimal_places=6)),
                ('context', models.ForeignKey(related_name='testsuite_context', default=None, blank=True, to='testdb.Key', null=True)),
                ('key', models.ForeignKey(related_name='testsuite_key', default=None, blank=True, to='testdb.Key', null=True)),
                ('testsuite', models.ForeignKey(default=None, blank=True, to='testdb.Testsuite', null=True)),
            ],
        ),
    ]
