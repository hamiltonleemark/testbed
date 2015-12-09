# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.DecimalField(max_digits=24, decimal_places=6)),
                ('context', models.ForeignKey(related_name='test_context', default=None, blank=True, to='testdb.Key', null=True)),
                ('key', models.ForeignKey(related_name='test_key', default=None, blank=True, to='testdb.Key', null=True)),
                ('test', models.ForeignKey(default=None, blank=True, to='testdb.Test', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='testresult',
            name='context',
        ),
        migrations.RemoveField(
            model_name='testresult',
            name='key',
        ),
        migrations.RemoveField(
            model_name='testresult',
            name='test',
        ),
        migrations.DeleteModel(
            name='TestResult',
        ),
    ]
