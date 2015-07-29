"""
  Create your tests here.
"""
from django.utils import timezone
from django.test import TestCase
from .models import Test
from .models import Testsuite
from .models import TestsuiteName
from .models import TestsuiteKeySet
from .models import Key
from .models import TestKey
from .models import Context


class TestsuiteTestCase(TestCase):
    """ Test various aspects of a testsuite. """

    def testsuite_create_basic(self):
        """ Test creating a testsuite. """

        start_time = timezone.now()

        context = Context.objects.create(name="default")
        key1 = Key.objects.create(value="key1")
        key2 = Key.objects.create(value="key2")
        keys = (TestKey.objects.create(key=key1, value="value1"),
                TestKey.objects.create(key=key2, value="value2"))

        name = TestsuiteName.objects.create(name="testsuite_name")
        testsuite = Testsuite.objects.create(name=name, context=context)
        for key in keys:
            TestsuiteKeySet.objects.create(testsuite=testsuite, testkey=key)
        testsuite.save()

        ##
        # Making sure auto assignment of current time for the timestamp field
        # is working.
        self.assertTrue(testsuite.timestamp >= start_time)

    def testsuite_create_method(self):
        """ Test creating a testsuite. """

        start_time = timezone.now()

        keys = (TestKey.get_or_create("key1", "value1")[0],
                TestKey.get_or_create("key2", "value2")[0])
        testsuite = Testsuite.get_or_create("default", "testsuite_name", keys)

        ##
        # Making sure auto assignment of current time for the timestamp field
        # is working.
        self.assertTrue(testsuite.timestamp >= start_time)

        testsuite1 = Testsuite.get_or_create("default", "testsuite_name", keys)
        self.assertTrue(testsuite1.timestamp >= start_time)

        self.assertTrue(testsuite.timestamp == testsuite1.timestamp)
        self.assertTrue(testsuite == testsuite1)

    def test_create_method(self):
        """ Test creating a testsuite. """

        keys = (TestKey.get_or_create("key1", "value1")[0],
                TestKey.get_or_create("key2", "value2")[0])
        testsuite = Testsuite.get_or_create("default", "testsuite_name1", keys)
        test1 = Test.get_or_create(testsuite, "test_name1", keys)
        test2 = Test.get_or_create(testsuite, "test_name2", keys)

        self.assertTrue(test1.id != test2.id)
