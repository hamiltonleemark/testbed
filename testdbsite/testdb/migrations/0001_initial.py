# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

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
                ('config_type', models.IntegerField(default=0, choices=[(0, b'ANY'), (1, b'STRICT')])),
            ],
        ),
        migrations.CreateModel(
            name='KVP',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=128)),
                ('key', models.ForeignKey(to='testdb.Key')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=0)),
                ('branch', models.ForeignKey(related_name='branch', to='testdb.Key')),
                ('context', models.ForeignKey(to='testdb.Context')),
            ],
        ),
        migrations.CreateModel(
            name='ProductKeySet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product', models.ForeignKey(to='testdb.Product')),
                ('testkey', models.ForeignKey(to='testdb.KVP')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(default=-1, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(unique=True, max_length=256)),
                ('key', models.ForeignKey(to='testdb.KVP')),
                ('testsuite', models.ForeignKey(default=None, blank=True, to='testdb.Test', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestKeySet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('test', models.ForeignKey(to='testdb.Test')),
                ('testkey', models.ForeignKey(to='testdb.KVP')),
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
            name='Testplan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('context', models.ForeignKey(to='testdb.Context')),
            ],
        ),
        migrations.CreateModel(
            name='TestplanKeySet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.ForeignKey(to='testdb.Key')),
                ('testplan', models.ForeignKey(to='testdb.Testplan')),
            ],
        ),
        migrations.CreateModel(
            name='TestplanOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=0)),
                ('testplan', models.ForeignKey(default=None, blank=True, to='testdb.Testplan', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.DecimalField(max_digits=24, decimal_places=6)),
                ('context', models.ForeignKey(related_name='test_context', default=None, blank=True, to='testdb.Key', null=True)),
                ('key', models.ForeignKey(related_name='test_key', default=None, blank=True, to='testdb.Key', null=True)),
                ('test', models.ForeignKey(default=None, blank=True, to='testdb.Test', null=True)),
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
                ('key', models.ForeignKey(to='testdb.KVP')),
                ('testsuite', models.ForeignKey(default=None, blank=True, to='testdb.Testsuite', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestsuiteKeySet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('testkey', models.ForeignKey(to='testdb.KVP')),
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
            field=models.ManyToManyField(to='testdb.KVP', through='testdb.TestsuiteKeySet'),
        ),
        migrations.AddField(
            model_name='testsuite',
            name='name',
            field=models.ForeignKey(to='testdb.TestsuiteName'),
        ),
        migrations.AddField(
            model_name='testsuite',
            name='testplanorder',
            field=models.ForeignKey(default=None, blank=True, to='testdb.TestplanOrder', null=True),
        ),
        migrations.AddField(
            model_name='testplan',
            name='keys',
            field=models.ManyToManyField(to='testdb.Key', through='testdb.TestplanKeySet'),
        ),
        migrations.AddField(
            model_name='test',
            name='keys',
            field=models.ManyToManyField(to='testdb.KVP', through='testdb.TestKeySet'),
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
            model_name='product',
            name='keys',
            field=models.ManyToManyField(to='testdb.KVP', through='testdb.ProductKeySet'),
        ),
        migrations.AddField(
            model_name='product',
            name='product',
            field=models.ForeignKey(related_name='product', to='testdb.Key'),
        ),
    ]
