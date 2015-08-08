# (c) 2015 Mark Hamilton, <mark_lee_hamilton@att.net>
#
# This file is part of testbed
#
# Testbed is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Testbed is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Testdb.  If not, see <http://www.gnu.org/licenses/>.
"""
   Test schema for tracking tests and their results.
"""
from django.utils import timezone
from django.db import models


class Key(models.Model):
    """ Key refers to a generic way to retrieve a value."""
    value = models.CharField(max_length=128, unique=True)

    def __str__(self):
        """ Return testsuite name. """
        return str(self.value)


class Result(models.Model):
    """ Define a single result. """
    context = models.ForeignKey(Key, related_name="context", null=True,
                                blank=True, default=None)
    key = models.ForeignKey(Key, related_name="key", null=True,
                            blank=True, default=None)
    value = models.DecimalField(max_digits=24, decimal_places=6)
    name = models.ForeignKey(Key)
    test = models.ForeignKey("Test", null=True, blank=True, default=None)


class TestKey(models.Model):
    """ Tests are associated to a set of keys. """
    key = models.ForeignKey(Key)
    value = models.CharField(max_length=128)

    def __str__(self):
        """ Return testsuite name. """
        return "%s=%s" % (self.key, self.value)

    @staticmethod
    def get_or_create(key, value):
        """ Create a single test key objects. """
        (key, _) = Key.objects.get_or_create(value=key)
        return TestKey.objects.get_or_create(key=key, value=value)

    @staticmethod
    def filter(contains):
        """ Filter testsuite against a single string. """

        if not contains:
            return TestKey.objects.all()

        return TestKey.objects.filter(
            models.Q(key__value__contains=contains) |
            models.Q(value__contains=contains))


class TestName(models.Model):
    """ Name of testsuite."""
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        """ Return testsuite name. """
        return str(self.name)


class Test(models.Model):
    """ A single test consisting of one or more results. """
    testsuite = models.ForeignKey("Testsuite", null=True, blank=True,
                                  default=None)
    name = models.ForeignKey(TestName)
    keys = models.ManyToManyField(TestKey, through="TestKeySet")
    status = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        """ User representation. """
        return "%s" % self.name

    @staticmethod
    def filter(contains):
        """ Filter testsuite against a single string. """

        if not contains:
            return Test.objects.all()

        return Test.objects.filter(
            models.Q(testsuite__context__name__contains=contains) |
            models.Q(testsuite__name__name__contains=contains) |
            models.Q(name__name__contains=contains))

    @staticmethod
    def get_or_create(testsuite, name, keys):
        """ Get current or create new objects.
        @param testkeys Must be an instance of TestKey.
        """

        (name, _) = TestName.objects.get_or_create(name=name)

        ##
        # Look for test.
        find = Test.objects.filter(testsuite=testsuite, name=name)
        for key in keys:
            find = find.filter(keys=key)

        if find.count() == 1:
            return [item for item in find][0]
        elif find.count() > 1:
            raise Test.MultipleObjectsReturned("%s" % (name))

        test = Test.objects.create(testsuite=testsuite, name=name)

        for key in keys:
            TestKeySet.objects.create(test=test, testkey=key)
        return test


class TestFile(models.Model):
    """ Hold a single file related to a testsuite. """
    testsuite = models.ForeignKey(Test, null=True, blank=True, default=None)
    key = models.ForeignKey(TestKey)
    path = models.CharField(max_length=256, unique=True)


class TestKeySet(models.Model):
    """ Links a test to a set of keys. """
    test = models.ForeignKey(Test)
    testkey = models.ForeignKey(TestKey)


class TestsuiteName(models.Model):
    """ Name of testsuite."""
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        """ Return testsuite name. """
        return str(self.name)


class Context(models.Model):
    """ A testsuite resides in an arbitrary context.
    A context is nothing more than a way to organize testsuites by a logical
    concept.
    """
    name = models.CharField(max_length=128, null=True, blank=True,
                            default=None)

    def __str__(self):
        return self.name


class Testsuite(models.Model):
    """ A Testsuite holds a set of tests. """

    context = models.ForeignKey(Context, null=True, blank=True, default=None)
    name = models.ForeignKey(TestsuiteName)
    timestamp = models.DateTimeField(default=timezone.now)
    keys = models.ManyToManyField(TestKey, through="TestsuiteKeySet")

    def __str__(self):
        """ User representation. """
        return "%s.%s" % (self.context, self.name)

    @staticmethod
    def filter(contains):
        """ Filter testsuite against a single string. """
        if not contains:
            return Testsuite.objects.all()
        return Testsuite.objects.filter(
            models.Q(context__name__contains=contains) |
            models.Q(name__name__contains=contains))

    @staticmethod
    def get_or_create(context, name, testkeys=None):
        """ Get current or create new objects.
        @param testkeys Must be an instance of TestKey.
        """
        if not testkeys:
            testkeys = []

        (context, _) = Context.objects.get_or_create(name=context)
        (name, _) = TestsuiteName.objects.get_or_create(name=name)

        ##
        # Look for testsuite.
        find = Testsuite.objects.filter(context=context, name=name)
        for testkey in testkeys:
            find = find.filter(keys=testkey)

        if find.count() == 1:
            return [item for item in find][0]
        elif find.count() > 1:
            raise Testsuite.MultipleObjectsReturned("%s %s" % (context, name))

        testsuite = Testsuite.objects.create(name=name, context=context)
        for testkey in testkeys:
            TestsuiteKeySet.objects.create(testsuite=testsuite,
                                           testkey=testkey)
        return testsuite


class TestsuiteFile(models.Model):
    """ Hold a single file related to a testsuite. """
    testsuite = models.ForeignKey(Testsuite, null=True, blank=True,
                                  default=None)
    key = models.ForeignKey(TestKey)
    path = models.CharField(max_length=256, unique=True)


class TestsuiteKeySet(models.Model):
    """ Testsuites are associated to a set of keys. """
    testsuite = models.ForeignKey(Testsuite)
    testkey = models.ForeignKey(TestKey)
