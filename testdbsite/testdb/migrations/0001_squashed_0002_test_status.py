# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [(b'testdb', '0001_initial'), (b'testdb', '0002_test_status')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Context',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=None, max_length=128, null=True, blank=True)),
            ],
        ),
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
                ('context', models.ForeignKey(related_name='context', default=None, blank=True, to='testdb.Key', null=True)),
                ('key', models.ForeignKey(related_name='key', default=None, blank=True, to='testdb.Key', null=True)),
                ('name', models.ForeignKey(to='testdb.Key')),
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
                ('key', models.ForeignKey(to='testdb.Key')),
            ],
        ),
        migrations.CreateModel(
            name='TestKeySet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('test', models.ForeignKey(to='testdb.Test')),
                ('testkey', models.ForeignKey(to='testdb.TestKey')),
            ],
        ),
        migrations.CreateModel(
            name='TestName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Testsuite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('context', models.ForeignKey(default=None, blank=True, to='testdb.Context', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestsuiteFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(unique=True, max_length=256)),
                ('key', models.ForeignKey(to='testdb.TestKey')),
                ('testsuite', models.ForeignKey(default=None, blank=True, to='testdb.Testsuite', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestsuiteKeySet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('testkey', models.ForeignKey(to='testdb.TestKey')),
                ('testsuite', models.ForeignKey(to='testdb.Testsuite')),
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
            name='keys',
            field=models.ManyToManyField(to=b'testdb.TestKey', through='testdb.TestsuiteKeySet'),
        ),
        migrations.AddField(
            model_name='testsuite',
            name='name',
            field=models.ForeignKey(to='testdb.TestsuiteName'),
        ),
        migrations.AddField(
            model_name='testfile',
            name='key',
            field=models.ForeignKey(to='testdb.TestKey'),
        ),
        migrations.AddField(
            model_name='testfile',
            name='testsuite',
            field=models.ForeignKey(default=None, blank=True, to='testdb.Test', null=True),
        ),
        migrations.AddField(
            model_name='test',
            name='keys',
            field=models.ManyToManyField(to=b'testdb.TestKey', through='testdb.TestKeySet'),
        ),
        migrations.AddField(
            model_name='test',
            name='name',
            field=models.ForeignKey(to='testdb.TestName'),
        ),
        migrations.AddField(
            model_name='test',
            name='testsuite',
            field=models.ForeignKey(default=None, blank=True, to='testdb.Testsuite', null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='test',
            field=models.ForeignKey(default=None, blank=True, to='testdb.Test', null=True),
        ),
        migrations.AddField(
            model_name='test',
            name='status',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
