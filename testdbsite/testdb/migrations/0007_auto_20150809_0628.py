# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0006_auto_20150809_0525'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testplan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=0)),
                ('testsuite', models.ForeignKey(default=None, blank=True, to='testdb.Testsuite', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='testsuiteresult',
            name='context',
        ),
        migrations.RemoveField(
            model_name='testsuiteresult',
            name='key',
        ),
        migrations.RemoveField(
            model_name='testsuiteresult',
            name='testsuite',
        ),
        migrations.DeleteModel(
            name='TestsuiteResult',
        ),
    ]
