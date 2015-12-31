# (c) 2015 Mark Hamilton, <mark.lee.hamilton@gmail.com>
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
    """ Identifies an associated list of values.

    For example, the key product could have the values ipod, ipad and walkman.
    The set of values are stored in the Values table.
    """

    CONFIG_TYPE_ANY = 0
    CONFIG_TYPE_STRICT = 1

    CONFIG_TYPE = {
        (CONFIG_TYPE_ANY, "ANY"),
        (CONFIG_TYPE_STRICT, "STRICT")
    }

    value = models.CharField(max_length=128, unique=True)
    config_type = models.IntegerField(choices=CONFIG_TYPE, default=0)

    @staticmethod
    def str_to_config_type(value):
        """ Return config_type given string. """
        for (config_type, config_str) in Key.CONFIG_TYPE:
            if value == config_str:
                return config_type
        raise ValueError("unknown: config_type %s", value)

    def __str__(self):
        """ Return testsuite name. """
        return str(self.value)


class KVP(models.Model):
    """ Key-Value Pair associate a key with a set of values. """

    key = models.ForeignKey(Key)
    value = models.CharField(max_length=128)

    def __str__(self):
        """ Return testsuite name. """
        return "%s=%s" % (self.key, self.value)

    @staticmethod
    def get(key, value):
        """ Retrieve KVP. """
        (key, _) = Key.objects.get_or_create(value=key)
        return KVP.objects.get(key=key, value=value)

    @staticmethod
    def get_or_create(key, value):
        """ Create a single test key objects. """

        (key, _) = Key.objects.get_or_create(value=key)

        try:
            testkey = KVP.objects.get(key=key, value=value)
            if testkey:
                return (testkey, False)
        except KVP.DoesNotExist:
            pass

        if key.config_type != Key.CONFIG_TYPE_ANY:
            raise KVP.DoesNotExist("key %s is strict" % key)
        return KVP.objects.get_or_create(key=key, value=value)

    @staticmethod
    def filter(contains):
        """ Filter testsuite against a single string. """

        if not contains:
            return KVP.objects.all()

        return KVP.objects.filter(
            models.Q(key__value__contains=contains) |
            models.Q(value__contains=contains))


class Result(models.Model):
    """ Define a single result. """
    context = models.ForeignKey(Key, related_name="test_context", null=True,
                                blank=True, default=None)
    key = models.ForeignKey(Key, related_name="test_key", null=True,
                            blank=True, default=None)
    value = models.DecimalField(max_digits=24, decimal_places=6)
    test = models.ForeignKey("Test", null=True, blank=True, default=None)


class TestName(models.Model):
    """ Name of testsuite."""
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        """ Return testsuite name. """
        return str(self.name)


class Test(models.Model):
    """ A single test consisting of one or more results. """
    PASS = 0
    FAIL = 1
    UNKNOWN = -1

    testsuite = models.ForeignKey("Testsuite", null=True, blank=True,
                                  default=None)
    name = models.ForeignKey(TestName)
    keys = models.ManyToManyField(KVP, through="TestKVP")
    status = models.IntegerField(default=-1, blank=True, null=True)

    # \todo key_get should return only Testkey to make effecient.
    def key_get(self, key):
        """ Return value given key. """
        return self.keys.get(key__value=key).value

    def name_get(self):
        """ Return test name. """
        return self.name.name

    def __str__(self):
        """ User representation. """
        return "%s" % self.name

    @staticmethod
    def status_to_str(status, short=False):
        """ Return string form of the status code. """
        if short:
            if status == Test.PASS:
                return "P"
            elif status == Test.FAIL:
                return "F"
        else:
            if status == Test.PASS:
                return "pass"
            elif status == Test.FAIL:
                return "fail"

    @staticmethod
    def status_map(status):
        """ Return status. """
        if status == "pass":
            return Test.PASS
        elif status == "fail":
            return Test.FAIL

    # \todo This should be named contains
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
    def get_or_create(testsuite, name, status, keys):
        """ Get current or create new objects.
        @param testkeys Must be an instance of KVP.
        @return (obj, created) created is a boolean. True if newly created.
        """

        status = Test.status_map(status)

        ##
        # \todo should be pulled out.
        (name, created) = TestName.objects.get_or_create(name=name)

        ##
        # Look for test.
        find = Test.objects.filter(testsuite=testsuite, name=name)
        for key in keys:
            find = find.filter(keys=key)

        if find.count() == 1:
            return ([item for item in find][0], created)
        elif find.count() > 1:
            raise Test.MultipleObjectsReturned(name)

        test = Test.objects.create(testsuite=testsuite, name=name,
                                   status=status)

        for key in keys:
            TestKVP.objects.create(test=test, testkey=key)

        return (test, True)

    def set_status(self, status):
        """ Set status. """
        if status == "pass":
            self.status = 0
        elif status == "fail":
            self.status = 1


class TestFile(models.Model):
    """ Hold a single file related to a testsuite. """

    test = models.ForeignKey(Test, null=True, blank=True, default=None)
    kvp = models.ForeignKey(KVP)
    path = models.CharField(max_length=256, unique=True)


class TestKVP(models.Model):
    """ Links a test to a set of keys. """
    test = models.ForeignKey(Test)
    kvp = models.ForeignKey(KVP)


class TestsuiteName(models.Model):
    """ Name of testsuite."""
    name = models.CharField(max_length=128, unique=True)

    def serialize(self, serializer):
        """ Serialize this object. """
        serializer.add(self)

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

    def serialize(self, serializer):
        """ Serialize this object. """
        serializer.add(self)

    def __str__(self):
        return self.name


class TestsuiteKVP(models.Model):
    """ Testsuites are associated to a set of keys. """
    testsuite = models.ForeignKey("Testsuite")
    kvp = models.ForeignKey(KVP)

    def __str__(self):
        """ User representation. """

        return "%s %s" % (str(self.testsuite.context), str(self.testkey))


class Testsuite(models.Model):
    """ A Testsuite holds a set of tests. """

    context = models.ForeignKey(Context, null=True, blank=True, default=None)
    name = models.ForeignKey(TestsuiteName)
    timestamp = models.DateTimeField(default=timezone.now)
    kvps = models.ManyToManyField(KVP, through="TestsuiteKVP")
    testplanorder = models.ForeignKey("TestplanOrder", null=True, blank=True,
                                      default=None)

    def serialize(self, serializer):
        """ Serialize this object and recursively foreign objects. """

        self.context.serialize(serializer)
        self.name.serialize(serializer)
        self.testplanorder.serialize(serializer)

        for item in self.testsuitekvp_set.all():
            serializer.add(item)

        serializer.add(self)

    def __str__(self):
        """ User representation. """
        return "%s.%s %s" % (self.context, self.name, self.timestamp)

    def name_get(self):
        """ Return the testsuite name. """
        return self.name.name

    def key_get(self, key):
        """ Return value given key. """
        return self.kvps.get(key__value=key)

    def key_remove(self, key):
        """ Remove key and return True if key exists and is removed. """
        try:
            keys = self.keys.filter(key__value=key)
            key = keys.first()
            key.delete()
            key.save()
            return True
        except Key.DoesNotExist:
            return False

    def key_change(self, testkey):
        """ Get/create/change KVP associated with this testsuite.
         Using the key either return the existing KVP if value matches,
         create a new KVP if one does not exist or change the existing key
         to the new value.
         """

        try:
            current_key = self.key_get(testkey.key.value)
            if current_key.value != testkey.value:
                current_key.delete()
                current_key.save()
                self.testsuitekvp_set.create(testkey=testkey)
        except KVP.DoesNotExist:
            self.testsuitekvp_set.create(kvp=testkey)

    def value_get(self, key, default=None):
        """ Return value given key. """
        try:
            testkvp = self.testsuitekvp_set.get(kvp__key__value=key)
            return testkvp.kvp.value
        except TestsuiteKVP.DoesNotExist:
            return default

    @staticmethod
    def contains(context, testsuite_name):
        """ Filter testsuite against a single string. """

        if context:
            find = Testsuite.objects.filter(context__name=context)
        else:
            find = Testsuite.objects.all()

        if not testsuite_name:
            return find

        return find.filter(name__name__contains=testsuite_name)

    @staticmethod
    def get_or_create(context, testsuite_name, testplanorder, buildkey,
                      testkeys):
        """ Get current or create new objects.

        @param testkeys Must be an instance of KVP.
        """
        if not testkeys:
            testkeys = []

        (context, created) = Context.objects.get_or_create(name=context)
        (name, critem) = TestsuiteName.objects.get_or_create(
            name=testsuite_name)
        created = created or critem

        ##
        # Look for testsuite
        find = Testsuite.objects.filter(context=context, name=name,
                                        testplanorder=testplanorder,
                                        kvps=buildkey)
        for testkey in testkeys:
            find = find.filter(kvps=testkey)

        if find.count() == 1:
            testsuite = find[0]
            results = (testsuite, created)
            return results
        elif find.count() > 1:
            raise Testsuite.MultipleObjectsReturned("%s %s" % (context, name))

        testsuite = Testsuite.objects.create(name=name, context=context,
                                             testplanorder=testplanorder)
        testkeys.append(buildkey)
        for testkey in testkeys:
            TestsuiteKVP.objects.create(testsuite=testsuite, kvp=testkey)
        return (testsuite, True)

    ##
    # \todo This is not making a lot of sense. Why is this filter
    # this should be a get maybe.
    @staticmethod
    def get(context, testplanorder, testkeys):
        """ List of testsuites based on testplan.
        @return Return a single Testsuite object.
        """

        find = Testsuite.objects.filter(context=context,
                                        testplanorder=testplanorder)

        if not testkeys:
            return find[0]
        ##
        # Look for testsuite.
        for testkey in testkeys[:-1]:
            find = find.filter(keys=testkey)
        results = [item for item in find.get(keys=testkeys[-1])]
        return results[0]

    ##
    # \todo This is not making a lot of sense. Why is this filter
    # this should be a get maybe.
    @staticmethod
    def filter(context, order, keys):
        """ List of testsuites based on testplan.
        @return Return a single Testsuite object.
        """

        find = Testsuite.objects.filter(context=context)

        if order:
            find = find.filter(testplanorder=order)

        if not keys:
            return find

        ##
        # Look for testsuite.
        for key in keys:
            find = find.filter(kvps=key)
        return find


class TestplanKVP(models.Model):
    """ Testsuites are associated to a set of keys. """

    testplan = models.ForeignKey("Testplan")
    key = models.ForeignKey(Key)


class Testplan(models.Model):
    """ A test plan consists of a set of testsuites and optionally tests.
    A test plan governs which testsuites should be run their results shown.
    """
    context = models.ForeignKey(Context)
    keys = models.ManyToManyField(Key, through="TestplanKVP")

    def serialize(self, serializer):
        """ Serialize and instance of this model. """
        self.context.serialize(serializer)
        serializer.add(self)

    def __str__(self):
        """ User representation. """
        return str(self.context)

    def testsuites_all(self):
        """ Testsuite set associated with this testplan.

        @return (order, testsuite)
        """
        for item in self.testplanorder_set.all().order_by("order"):
            yield (item.order, item.testsuite_set.all()[0])

    @staticmethod
    def context_get(context):
        """ Return the testplan full context name. """
        return Context.objects.get_or_create(name="testplan."+context)[0]

    # /todo this should be named update_or_create
    @staticmethod
    def get_or_create(context, keys=None):
        """ Get current or create new objects.
        @param context is a reference to a Context object returned from
               context_get.
        @param testkeys Must be an instance of KVP.
        """
        (testplan, critem) = Testplan.objects.get_or_create(context=context)

        if not critem:
            return (testplan, critem)

        for key in keys:
            testplan.testplankvp_set.create(key=key)
        return (testplan, critem)


class TestplanOrder(models.Model):
    """ Controls the order of the testsuite in the testplan. """

    testplan = models.ForeignKey(Testplan, null=True, blank=True,
                                 default=None)
    order = models.IntegerField(default=0)

    def serialize(self, serializer):
        """ Serialize this object. """
        self.testplan.serialize(serializer)
        serializer.add(self)

    def testsuite_name(self):
        """ Return the name of the testsuite. """
        return self.testsuite_set.first()

    def __str__(self):
        """ User representation. """
        return "%d: %s:" % (self.order, self.testplan.context)

    @staticmethod
    def get_or_create(testplan, testsuite_name, order):
        """ Get current testplan or create new objects. """

        created = False
        try:
            testplanorder = TestplanOrder.objects.get(
                testplan=testplan, testsuite__context=testplan.context,
                testsuite__name=testsuite_name)
            testsuite = Testsuite.objects.get(context=testplan.context,
                                              testplanorder=testplanorder)
        except TestplanOrder.DoesNotExist:
            testplanorder = TestplanOrder.objects.create(testplan=testplan,
                                                         order=order)
            testsuite = Testsuite.objects.create(context=testplan.context,
                                                 name=testsuite_name,
                                                 testplanorder=testplanorder)
            created = True
        return (testplanorder, testsuite, created)

    @staticmethod
    def create(testplan, testsuite_name, order):
        """ Get current or create new objects. """

        testplanorder = TestplanOrder.objects.create(testplan=testplan,
                                                     order=order)
        testsuite = Testsuite.objects.create(context=testplan.context,
                                             name=testsuite_name,
                                             testplanorder=testplanorder)
        return (testplanorder, testsuite)

    @staticmethod
    def get(testplan, testsuite_name):
        """ Get current testplan or create new objects. """

        testplanorder = TestplanOrder.objects.get(
            testplan=testplan, testsuite__context=testplan.context,
            testsuite__name=testsuite_name)
        try:
            testsuite = Testsuite.objects.get(context=testplan.context,
                                              testplanorder=testplanorder)
        except Testsuite.DoesNotExist:
            raise TestplanOrder.DoesNotExist("missing testsuite %s",
                                             testsuite.name)
        return (testplanorder, testsuite)


class TestsuiteFile(models.Model):
    """ Hold a single file related to a testsuite. """
    testsuite = models.ForeignKey(Testsuite, null=True, blank=True,
                                  default=None)
    kvp = models.ForeignKey(KVP)
    path = models.CharField(max_length=256, unique=True)


class ProductKVP(models.Model):
    """ Testsuites are associated to a set of keys. """

    product = models.ForeignKey("Product")
    kvp = models.ForeignKey(KVP)


class Product(models.Model):
    """ A test plan consists of a set of testsuites, tests.
    A test plan governs which testsuites should be run.
    """

    context = models.ForeignKey(Context)
    product = models.ForeignKey(Key, related_name="product")
    branch = models.ForeignKey(Key, related_name="branch")
    kvps = models.ManyToManyField(KVP, through="ProductKVP")
    order = models.IntegerField(default=0)

    def __str__(self):
        """ User representation. """
        return "%d: %s %s %s" % (self.order, self.context, self.product,
                                 self.branch)

    # \todo Rename this to value_get
    def key_get(self, key, default=None):
        """ Return value given key. """

        try:
            return self.kvps.get(key__value=key).value
        except KVP.DoesNotExist:
            return default

    def key_get_or_create(self, key, value):
        """ Add key to product. """

        (kvp, _) = KVP.get_or_create(key, value)
        return self.productkvp_set.get_or_create(kvp=kvp)

    @staticmethod
    def get_or_create(context, product, branch, testkeys=None):
        """ Get current or create new objects.
        @param testkeys Must be an instance of KVP.
        """
        if not testkeys:
            testkeys = []

        (context, _) = Context.objects.get_or_create(name=context)
        (product, _) = Key.objects.get_or_create(value=product)
        (branch, _) = Key.objects.get_or_create(value=branch)

        ##
        # Look for testsuite.
        find = Product.objects.filter(context=context, product=product,
                                      branch=branch)
        for testkey in testkeys:
            find = find.filter(keys=testkey)

        if find.count() == 1:
            return ([item for item in find][0], False)
        elif find.count() > 1:
            raise Testsuite.MultipleObjectsReturned("%s %s %s" % (context,
                                                                  product,
                                                                  branch))

        product = Product.objects.create(context=context, product=product,
                                         branch=branch)
        for testkey in testkeys:
            ProductKVP.objects.create(product=product, testkey=testkey)
        return (product, True)

    @staticmethod
    def filter(context, contains):
        """ Filter testsuite against a single string. """

        if context:
            (context, _) = Context.objects.get_or_create(name=context)
            find = Product.objects.filter(context=context)
        else:
            find = Product.objects.all()

        if contains:
            find = find.filter(models.Q(product__value__contains=contains) |
                               models.Q(branch__value__contains=contains) |
                               models.Q(kvps__key__value__contains=contains))
        return find.order_by("context", "order")

    @staticmethod
    def get(context, product, branch, testkeys=None):
        """ Get current or create new objects.

        @param testkeys Must be an instance of KVP.
        """
        if not testkeys:
            testkeys = []

        context = Context.objects.get(name=context)
        try:
            product = Key.objects.get(value=product)
        except Key.DoesNotExist:
            raise Key.DoesNotExist("DoesNotExist: product %s does not exist" %
                                   product)
        try:
            branch = Key.objects.get(value=branch)
        except Key.DoesNotExist:
            raise Key.DoesNotExist("DoesNotExist: branch %s does not exist" %
                                   branch)

        ##
        # Look for testsuite.
        find = Product.objects.filter(context=context, product=product,
                                      branch=branch)
        for testkey in testkeys:
            find = find.filter(keys=testkey)

        if find.count() == 1:
            return [item for item in find][0]
        elif find.count() > 1:
            raise Product.MultipleObjectsReturned("%s %s %s" % (context,
                                                                product,
                                                                branch))
        else:
            raise Product.DoesNotExist("%s %s %s" % (context, product, branch))
