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
  Create your tests here.
"""
from django.utils import timezone
from django.test import TestCase
from .models import Test
from .models import Testsuite
from .models import TestsuiteName
from .models import TestsuiteKeySet
from .models import Key
from .models import KVP
from .models import Context
from .models import Testplan
from .models import TestplanOrder


class TestsuiteTestCase(TestCase):
    """ Test various aspects of a testsuite. """

    def testsuite_basic(self):
        """ Test creating a testsuite. """

        start_time = timezone.now()

        context = Context.objects.create(name="default")
        key1 = Key.objects.create(value="key1")
        key2 = Key.objects.create(value="key2")
        keys = (KVP.objects.create(key=key1, value="value1"),
                KVP.objects.create(key=key2, value="value2"))

        name = TestsuiteName.objects.create(name="testsuite_name")
        testsuite = Testsuite.objects.create(name=name, context=context)
        for key in keys:
            TestsuiteKeySet.objects.create(testsuite=testsuite, testkey=key)
        testsuite.save()

        ##
        # Making sure auto assignment of current time for the timestamp field
        # is working.
        self.assertTrue(testsuite.timestamp >= start_time)

    def testsuite_create(self):
        """ testsuite_create Test creating a testsuite. """

        start_time = timezone.now()

        keys = [KVP.get_or_create("key1", "value1")[0],
                KVP.get_or_create("key2", "value2")[0]]
        buildkey = KVP.get_or_create("build", "build1")[0]
        (testsuite, _) = Testsuite.get_or_create("default", "testsuite_name",
                                                 None, buildkey, keys)

        ##
        # Making sure auto assignment of current time for the timestamp field
        # is working.
        self.assertTrue(testsuite.timestamp >= start_time)

        (testsuite1, _) = Testsuite.get_or_create("default", "testsuite_name",
                                                  None, buildkey, keys)
        self.assertTrue(testsuite1.timestamp >= start_time)

        self.assertTrue(testsuite.timestamp == testsuite1.timestamp)
        self.assertTrue(testsuite == testsuite1)

    def test_create_method(self):
        """ Test creating a testsuite. """

        keys = [KVP.get_or_create("key1", "value1")[0],
                KVP.get_or_create("key2", "value2")[0]]
        buildkey = KVP.get_or_create("build", "build1")[0]

        (testsuite, _) = Testsuite.get_or_create("default", "testsuite_name1",
                                                 None, buildkey, keys)
        (test1, _) = Test.get_or_create(testsuite, "test_name1", "pass", [])
        (test2, _) = Test.get_or_create(testsuite, "test_name2", "pass", [])

        self.assertTrue(test1.id != test2.id)

    def testplan_order(self):
        """ Test the creation and order support of test plan. """

        test_keys = [KVP.get_or_create("key1", "value1.1")[0]]
        build_key = KVP.get_or_create("build", "build1")[0]

        (testplan, rtc) = Testplan.get_or_create("testplan.default", test_keys)
        self.assertTrue(rtc, "testplan not created")

        (testplanorder, rtc) = TestplanOrder.objects.get_or_create(
            testplan=testplan, order=1)
        self.assertTrue(rtc, "testplanorder not created")

        (_, rtc) = Testsuite.get_or_create("testplan.default", "testsuite1",
                                           testplanorder, build_key, [])
        self.assertTrue(rtc, "testsuite1 not created")

        (testplanorder, rtc) = TestplanOrder.objects.get_or_create(
            testplan=testplan, order=2)
        (_, rtc) = Testsuite.get_or_create("default", "testsuite2",
                                           testplanorder, build_key, [])
        self.assertTrue(rtc, "testsuite2 not created")
        testplans = TestplanOrder.objects.order_by("order")
        testsuites = [Testsuite.objects.get(testplanorder=item)
                      for item in testplans]
        self.assertEqual(testsuites[0].name.name, "testsuite1")
        self.assertEqual(testsuites[1].name.name, "testsuite2")
