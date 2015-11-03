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
Test test functionality.
"""
import datetime
import argparse
from django.test import TestCase
from . import commands
from . import api
from testbed.libexec import build
from testbed.libexec import testsuite
from testbed.libexec import testplan


# pylint: disable=R0914
# pylint: disable=R0915
class TestTestCase(TestCase):
    """ Tests for Django backend.

    These test must derive from django.test.TestCase. """

    @staticmethod
    def parser_create():
        """ Create sub parser. """

        arg_parser = argparse.ArgumentParser(prog="tbd")
        subparser = arg_parser.add_subparsers(title="subcommands")
        commands.add_subparser(subparser)
        return arg_parser

    def test_commands_large(self):
        """ test_commands_large: Check the time for handling a lot of tests.
        """
        from testdb import models

        build_count = 10
        testsuite_count = 100
        test_count = 1

        testkeys = [
            ("key1", "value1"),
            ("key2", "value2"),
            ("key3", "value3"),
            ("key4", "value4"),
            ("product", "product1"),
            ("branch", "branch1"),
        ]

        ##
        # Create testplan.
        for item in range(0, testsuite_count):
            name = "testsuite%d" % item
            (_, created) = testplan.api.get_or_create(testplan.api.CONTEXT,
                                                      name, item)
            self.assertTrue(created, "created testsuite%d" % item)

        print "MARK:testplan", testplan.api.CONTEXT
        context = models.Testplan.context_get(testplan.api.CONTEXT)
        testplan1 = models.Testplan.objects.get(context=context)

        find = testplan1.testplanorder_set.all()
        self.assertEqual(find.count(), testsuite_count)

        for testkey in testkeys:
            (testkey, _) = models.KVP.get_or_create(key=testkey[0],
                                                    value=testkey[1])
            testplan1.testplankeyset_set.get_or_create(testplan=testplan1,
                                                       testkey=testkey)

        orders = testplan1.testplanorder_set.all().order_by("order")
        self.assertEqual(len(orders), testsuite_count)
        for order in orders:
            self.assertEqual(order.testsuite_set.all().count(), 1)
        #
        ##

        ##
        # Create build content as in a history.
        start = datetime.datetime.now()
        for bitem in range(0, build_count):
            buildid = "build%d" % bitem
            build.api.get_or_create("product1", "branch1", buildid)

            for titem in range(0, testsuite_count):
                (_, rtc) = testsuite.api.add_testsuite("default",
                                                       "testsuite%d" % titem,
                                                       buildid, testkeys)
                self.assertTrue(rtc, "new test not created")
                for testitem in range(0, test_count):
                    print "MARK: testitem", testitem
                    (_, rtc) = api.set_result("default", "product1", "branch1",
                                              buildid, "testsuite%d" % titem,
                                              "test%d" % testitem, "pass",
                                              testkeys)
                    print "MARK: rtc", rtc
                    self.assertTrue(rtc, "result not created")
        end = datetime.datetime.now()

        duration = end - start
        print "\ncreated testsuite %d %s" % (testsuite_count, duration)
        results = [item for item in api.list_result("default", [])]
        self.assertEqual(len(results), build_count*testsuite_count*test_count)
        #
        ##

        ##
        # Time retrieving all testsuites.
        start = datetime.datetime.now()
        testkeys = [item.testkey
                    for item in testplan1.testplankeyset_set.all()]
        (buildkey, _) = models.KVP.get_or_create("build", "build1")

        testkeys.append(buildkey)
        self.assertEqual(len(orders), testsuite_count)
        results = [item for item in testsuite.api.list_testsuite("default",
                                                                 testkeys)]
        end = datetime.datetime.now()
        duration = end - start
        self.assertEqual(len(results), testsuite_count)
        self.assertTrue(duration.seconds < 1.0, "query is taking too long.")
        print "testsuite search %d duration %s" % (testsuite_count, duration)
        ##

        ##
        # Time to retrieving all test results
        start = datetime.datetime.now()
        results = [item for item in api.list_result("default", testkeys)]
        end = datetime.datetime.now()
        duration = end - start
        print "test search %d duration %s" % (testsuite_count, duration)
        self.assertTrue(duration.seconds < 1.0, "query is taking too long.")
        self.assertEqual(len(results), testsuite_count*test_count)
