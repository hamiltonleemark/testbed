# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Key',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(unique=True, max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.DecimalField(max_digits=24, decimal_places=6)),
                ('contenxt', models.ForeignKey(related_name='context', default=None, blank=True, to='tests.Key', null=True)),
                ('key', models.ForeignKey(related_name='key', default=None, blank=True, to='tests.Key', null=True)),
                ('name', models.ForeignKey(to='tests.Key')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(unique=True, max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='TestKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=128)),
                ('key', models.ForeignKey(to='tests.Key')),
            ],
        ),
        migrations.CreateModel(
            name='TestKeySet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('test', models.ForeignKey(to='tests.Test')),
                ('testkey', models.ForeignKey(to='tests.TestKey')),
            ],
        ),
        migrations.CreateModel(
            name='Testsuite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='TestsuiteContext',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=None, max_length=128, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestsuiteFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(unique=True, max_length=256)),
                ('key', models.ForeignKey(to='tests.TestKey')),
                ('testsuite', models.ForeignKey(default=None, blank=True, to='tests.Testsuite', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestsuiteKeySet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('testkey', models.ForeignKey(to='tests.TestKey')),
                ('testsuite', models.ForeignKey(to='tests.Testsuite')),
            ],
        ),
        migrations.CreateModel(
            name='TestsuiteName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
            ],
        ),
        migrations.AddField(
            model_name='testsuite',
            name='context',
            field=models.ForeignKey(default=None, blank=True, to='tests.TestsuiteContext', null=True),
        ),
        migrations.AddField(
            model_name='testsuite',
            name='key',
            field=models.ManyToManyField(to='tests.TestKey', through='tests.TestsuiteKeySet'),
        ),
        migrations.AddField(
            model_name='testsuite',
            name='name',
            field=models.ForeignKey(to='tests.TestsuiteName'),
        ),
        migrations.AddField(
            model_name='testfile',
            name='key',
            field=models.ForeignKey(to='tests.TestKey'),
        ),
        migrations.AddField(
            model_name='testfile',
            name='testsuite',
            field=models.ForeignKey(default=None, blank=True, to='tests.Test', null=True),
        ),
        migrations.AddField(
            model_name='test',
            name='key',
            field=models.ManyToManyField(to='tests.TestKey', through='tests.TestKeySet'),
        ),
        migrations.AddField(
            model_name='test',
            name='name',
            field=models.ForeignKey(related_name='name', to='tests.Key'),
        ),
        migrations.AddField(
            model_name='test',
            name='testsuite',
            field=models.ForeignKey(default=None, blank=True, to='tests.Testsuite', null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='test',
            field=models.ForeignKey(default=None, blank=True, to='tests.Test', null=True),
        ),
    ]
