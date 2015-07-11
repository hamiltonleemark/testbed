"""
   Test schema for tracking tests and their results.
"""
from django.utils import timezone
from django.db import models


class Key(models.Model):
    """ Key refers to a generic way to retrieve a value."""
    value = models.CharField(max_length=128, unique=True)


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

    @staticmethod
    def get_or_create(key, value):
        """ Create a single test key objects. """
        (key, _) = Key.objects.get_or_create(value=key)
        return TestKey.objects.get_or_create(key=key, value=value)


class Test(models.Model):
    """ A single test consisting of one or more results. """
    testsuite = models.ForeignKey("Testsuite", null=True, blank=True,
                                  default=None)
    name = models.ForeignKey(Key, related_name="name")
    keys = models.ManyToManyField(TestKey, through="TestKeySet")

    @staticmethod
    def get_or_create(testsuite_name, keys, value):
        """ Create a single test key objects. """
        (testsuite, _) = Testsuite.objects.get_or_create(testsuite_name=testsuite_name)
        (key, _) = Key.objects.get_or_create(value=key)
        return TestKey.objects.get_or_create(key=key, value=value)



class TestFile(models.Model):
    """ Hold a single file related to a testsuite. """
    testsuite = models.ForeignKey(Test, null=True, blank=True, default=None)
    key = models.ForeignKey(TestKey)
    path = models.CharField(max_length=256, unique=True)


class TestKeySet(models.Model):
    """ Links a test to a set of keys. """
    testkey = models.ForeignKey(TestKey)
    test = models.ForeignKey(Test)


class TestsuiteName(models.Model):
    """ Name of testsuite."""
    name = models.CharField(max_length=128, unique=True)


class Context(models.Model):
    """ A testsuite resides in an arbitrary context.
    A context is nothing more than a way to organize testsuites by a logical
    concept.
    """
    name = models.CharField(max_length=128, null=True, blank=True,
                            default=None)


class Testsuite(models.Model):
    """ A Testsuite holds a set of tests. """
    context = models.ForeignKey(Context, null=True, blank=True, default=None)
    name = models.ForeignKey(TestsuiteName)
    timestamp = models.DateTimeField(default=timezone.now)
    keys = models.ManyToManyField(TestKey, through="TestsuiteKeySet")

    @staticmethod
    def get_or_create(context, name, testkeys):
        """ Get current or create new objects.
        @param testkeys Must be an instance of TestKey.
        """

        (context, _) = Context.objects.get_or_create(name=context)
        (name, _) = TestsuiteName.objects.get_or_create(name=name)

        ##
        # Look for testsuite.
        find = Testsuite.objects.filter(name=name, context=context)
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
    testkey = models.ForeignKey(TestKey)
    testsuite = models.ForeignKey(Testsuite)
