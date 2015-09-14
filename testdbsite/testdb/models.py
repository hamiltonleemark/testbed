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


# pylint: disable=E1101
class Key(models.Model):
    """ Key refers to a generic way to retrieve a value."""

    CONFIG_TYPE_ANY = 0
    CONFIG_TYPE_STRICT = 1

    CONFIG_TYPE = {
        (CONFIG_TYPE_ANY, "ANY"),
        (CONFIG_TYPE_STRICT, "STRICT")
    }

    value = models.CharField(max_length=128, unique=True)
    config_type = models.IntegerField(choices=CONFIG_TYPE, default=0)

    def __str__(self):
        """ Return testsuite name. """
        return str(self.value)


class TestResult(models.Model):
    """ Define a single result. """
    context = models.ForeignKey(Key, related_name="test_context", null=True,
                                blank=True, default=None)
    key = models.ForeignKey(Key, related_name="test_key", null=True,
                            blank=True, default=None)
    value = models.DecimalField(max_digits=24, decimal_places=6)
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
        try:
            testkey = TestKey.objects.get(key=key, value=value)
            if testkey:
                return (testkey, False)
        except TestKey.DoesNotExist:
            pass
        if key.config_type != Key.CONFIG_TYPE_ANY:
            raise TestKey.DoesNotExist("key %s is strict" % key)
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
    status = models.IntegerField(default=-1, blank=True, null=True)

    def key_get(self, key):
        """ Return value given key. """
        return self.keys.get(key__value=key).value

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
        @return (obj, created) created is a boolean. True if newly created.
        """

        (name, _) = TestName.objects.get_or_create(name=name)

        ##
        # Look for test.
        find = Test.objects.filter(testsuite=testsuite, name=name)
        for key in keys:
            find = find.filter(keys=key)

        if find.count() == 1:
            return ([item for item in find][0], False)
        elif find.count() > 1:
            raise Test.MultipleObjectsReturned(name)

        test = Test.objects.create(testsuite=testsuite, name=name)

        for key in keys:
            TestKeySet.objects.create(test=test, testkey=key)
        return (test, True)


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


class TestsuiteKeySet(models.Model):
    """ Testsuites are associated to a set of keys. """
    testsuite = models.ForeignKey("Testsuite")
    testkey = models.ForeignKey(TestKey)


class Testsuite(models.Model):
    """ A Testsuite holds a set of tests. """

    context = models.ForeignKey(Context, null=True, blank=True, default=None)
    name = models.ForeignKey(TestsuiteName)
    timestamp = models.DateTimeField(default=timezone.now)
    keys = models.ManyToManyField(TestKey, through="TestsuiteKeySet")
    testplanorder = models.ForeignKey("TestplanOrder", null=True, blank=True,
                                      default=None, related_name="order")

    def __str__(self):
        """ User representation. """

        return "%s.%s" % (self.context, self.name)

    def key_get(self, key):
        """ Return value given key. """
        return self.keys.get(key__value=key).value

    @staticmethod
    def filter(context, contains):
        """ Filter testsuite against a single string. """

        if context:
            find = Testsuite.objects.filter(context__name=context)
        else:
            find = Testsuite.objects.all()

        if not contains:
            return find
        return find.filter(name__name__contains=contains)

    @staticmethod
    def get_or_create(context, testsuite_name, testplanorder, testkeys=None):
        """ Get current or create new objects.

        @param testkeys Must be an instance of TestKey.
        """
        if not testkeys:
            testkeys = []

        (context, _) = Context.objects.get_or_create(name=context)
        (name, _) = TestsuiteName.objects.get_or_create(name=testsuite_name)

        ##
        # Look for testsuite.
        find = Testsuite.objects.filter(context=context, name=name)
        for testkey in testkeys:
            find = find.filter(keys=testkey)

        if find.count() == 1:
            return ([item for item in find][0], False)
        elif find.count() > 1:
            raise Testsuite.MultipleObjectsReturned("%s %s" % (context, name))

        testsuite = Testsuite.objects.create(name=name, context=context,
                                             testplanorder=testplanorder)
        for testkey in testkeys:
            TestsuiteKeySet.objects.create(testsuite=testsuite,
                                           testkey=testkey)
        return (testsuite, True)


class TestplanKeySet(models.Model):
    """ Testsuites are associated to a set of keys. """

    testplan = models.ForeignKey("Testplan")
    testkey = models.ForeignKey(TestKey)


class Testplan(models.Model):
    """ A test plan consists of a set of testsuites and optionally tests.
    A test plan governs which testsuites should be run their results shown.
    """
    context = models.ForeignKey(Context)
    keys = models.ManyToManyField(TestKey, through="TestplanKeySet")

    def __str__(self):
        """ User representation. """
        return str(self.context)

    def key_get(self, key):
        """ Return value given key. """
        return self.testsuite.key_get(key)

    @staticmethod
    def get_or_create(context, testkeys=None):
        """ Get current or create new objects.
        @param testkeys Must be an instance of TestKey.
        """
        if not testkeys:
            testkeys = []

        (context, _) = Context.objects.get_or_create(name=context)

        ##
        # Look for testsuite.
        find = Testplan.objects.filter(context=context)
        for testkey in testkeys:
            find = find.filter(keys=testkey)

        if find.count() == 1:
            return ([item for item in find][0], False)
        elif find.count() > 1:
            raise Testsuite.MultipleObjectsReturned(str(context))

        testplan = Testplan.objects.create(context=context)
        for testkey in testkeys:
            TestplanKeySet.objects.create(testplan=testplan, testkey=testkey)
        return (testplan, True)


class TestplanOrder(models.Model):
    """ Controls the order of the testsuite in the testplan. """
    testsuite = models.OneToOneField(Testsuite, primary_key=True,
                                     related_name="testsuite")
    order = models.IntegerField(default=0)
    testplan = models.ForeignKey(Testplan, null=True, blank=True, default=None)

    @staticmethod
    def get_or_create(testplan, testsuite, order):
        """ Get current or create new objects. """

        results = TestplanOrder.objects.get_or_create(testsuite=testsuite,
                                                      testplan=testplan)
        results[0].order = order

        results[0].save()
        return results


class TestsuiteFile(models.Model):
    """ Hold a single file related to a testsuite. """
    testsuite = models.ForeignKey(Testsuite, null=True, blank=True,
                                  default=None)
    key = models.ForeignKey(TestKey)
    path = models.CharField(max_length=256, unique=True)


class TestProductKeySet(models.Model):
    """ Testsuites are associated to a set of keys. """

    testproduct = models.ForeignKey("TestProduct")
    testkey = models.ForeignKey(TestKey)


class TestProduct(models.Model):
    """ A test plan consists of a set of testsuites, tests.
    A test plan governs which testsuites should be run.
    """

    context = models.ForeignKey(Context)
    product = models.ForeignKey(Key, related_name="product")
    branch = models.ForeignKey(Key, related_name="branch")
    keys = models.ManyToManyField(TestKey, through="TestProductKeySet")
    order = models.IntegerField(default=0)

    def __str__(self):
        """ User representation. """
        return "%d: %s %s" % (self.order, self.context,
                              self.key_get("product", "NA"))

    def key_get(self, key, default=None):
        """ Return value given key. """
        try:
            return self.keys.get(key__value=key).value
        except TestKey.DoesNotExist:
            return default

    @staticmethod
    def get_or_create(context, product, branch, testkeys=None):
        """ Get current or create new objects.
        @param testkeys Must be an instance of TestKey.
        """
        if not testkeys:
            testkeys = []

        (context, _) = Context.objects.get_or_create(name=context)
        (product, _) = Key.objects.get_or_create(value=product)
        (branch, _) = Key.objects.get_or_create(value=branch)

        ##
        # Look for testsuite.
        find = TestProduct.objects.filter(context=context, product=product,
                                          branch=branch)
        for testkey in testkeys:
            find = find.filter(keys=testkey)

        if find.count() == 1:
            return ([item for item in find][0], False)
        elif find.count() > 1:
            raise Testsuite.MultipleObjectsReturned("%s %s %s" % (context,
                                                                  product,
                                                                  branch))

        product = TestProduct.objects.create(context=context,
                                             product=product,
                                             branch=branch)
        for testkey in testkeys:
            TestProductKeySet.objects.create(testproduct=product,
                                             testkey=testkey)
        return (product, True)

    @staticmethod
    def filter(context, contains):
        """ Filter testsuite against a single string. """

        if context:
            (context, _) = Context.objects.get_or_create(name=context)
            find = TestProduct.objects.filter(context=context)
        else:
            find = TestProduct.objects.all()

        if contains:
            find = find.filter(models.Q(product__value__contains=contains) |
                               models.Q(branch__value__contains=contains) |
                               models.Q(keys__key__value__contains=contains))
        return find.order_by("context", "order")
