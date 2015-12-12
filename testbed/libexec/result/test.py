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
from testbed.libexec import product


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
        test_count = 5

        testkeys = [
            ("key1", "value1"),
            ("key2", "value2"),
        ]

        ##
        # Create testplan.
        for item in range(0, testsuite_count):
            testsuite_name = "testsuite%d" % item
            (_, testsuite1, created) = testplan.api.get_or_create(
                "default", testsuite_name, item)
            self.assertTrue(created, "created testsuite%d" % item)

            for testkey in testkeys:
                (_, critem) = testplan.api.add_key("default", item,
                                                   testkey[0], testkey[1])
                self.assertTrue(critem, "testsuite%d key not created" % item)

            for testitem in range(0, test_count):
                test_name = "test%d" % testitem
                models.Test.get_or_create(testsuite1, test_name, "pass", [])

        context = models.Testplan.context_get("default")
        testplan1 = models.Testplan.objects.get(context=context)
        self.assertTrue(testplan1 is not None, "testplan not created")

        find = testplan1.testplanorder_set.all().order_by("order")
        self.assertEqual(find.count(), testsuite_count)

        for testkey in testkeys:
            (key, _) = models.Key.objects.get_or_create(value=testkey[0])
            testplan1.testplankvp_set.get_or_create(testplan=testplan1,
                                                    key=key)

        orders = testplan1.testplanorder_set.all().order_by("order")
        self.assertEqual(len(orders), testsuite_count)
        for order in orders:
            self.assertEqual(order.testsuite_set.all().count(), 1)
        #
        ##

        ##
        # Create product and associate default test plan to product.
        product.api.get_or_create("product1", "branch1")
        product.api.add_testplan("product1", "branch1", "default")

        ##
        # Create build content as in a history.
        start = datetime.datetime.now()
        for bitem in range(0, build_count):
            buildid = "build%d" % bitem
            (_, rtc) = build.api.get_or_create("product1", "branch1", buildid)
            self.assertTrue(rtc, "new build not created")

            for titem in range(0, testsuite_count):
                testsuite_name = "testsuite%d" % titem
                (testsuite1, rtc) = testsuite.api.add_testsuite(
                    "default", "default", testsuite_name, buildid, testkeys)
                self.assertTrue(rtc, "new test not created")
                for testitem in range(0, test_count):
                    test_name = "test%d" % testitem
                    (_, rtc) = models.Test.get_or_create(testsuite1, test_name,
                                                         "pass", [])
                    self.assertTrue(rtc, "result not created")
        end = datetime.datetime.now()

        duration = end - start
        print "\ncreated testsuite %d %s" % (testsuite_count, duration)
        results = [item for item in api.list_result("default", "product1",
                                                    "branch1", [], None)]
        self.assertEqual(len(results), build_count*testsuite_count*test_count)
        #
        ##

        ##
        # These builds should not exist. Results should be zero.
        buildid = "build99"
        build.api.get_or_create("product1", "branch1", buildid)
        results = [item for item in testplan.api.list_testsuite("default", [],
                                                                buildid)]
        self.assertEqual(len(results), 0, "%s found %d." % (buildid,
                                                            len(results)))
        ##

        ##
        # Time retrieving all testsuites for a build1.
        start = datetime.datetime.now()
        testkeys = [item.key for item in testplan1.testplankvp_set.all()]
        (buildkey, _) = models.KVP.get_or_create("build", "build1")

        testkeys.append(buildkey)
        self.assertEqual(len(orders), testsuite_count)
        results = [item for item in testplan.api.list_testsuite("default", [],
                                                                "build1")]
        end = datetime.datetime.now()
        duration = end - start
        self.assertEqual(len(results), testsuite_count,
                         "build1 missing results")
        self.assertTrue(duration.seconds < 0.6, "query is taking too long.")
        print "testsuite search %d duration %s" % (testsuite_count, duration)
        ##

        ##
        # Time retrieving all testsuites from multiple builds.
        start = datetime.datetime.now()
        results = []
        for bitem in range(0, build_count):
            buildid = "build%d" % bitem
            results += [item for item in testplan.api.list_testsuite(
                "default", [], buildid)]
        end = datetime.datetime.now()
        duration = end - start
        self.assertEqual(len(results), build_count*testsuite_count,
                         "%d build results %d expected %d" %
                         (build_count, len(results),
                          build_count*testsuite_count))
        self.assertTrue(duration.seconds <= 1.0,
                        "query for %d is taking too long %f." %
                        (len(results), duration.seconds))
        print "search 5 builds %d duration %s" % (len(results), duration)
        ##

        ##
        # Time to retrieving all test results
        start = datetime.datetime.now()
        results = [item for item in api.list_result("default", "product1",
                                                    "branch1", [], None)]
        end = datetime.datetime.now()
        duration = end - start
        print "search all results duration %s" % (duration)
        self.assertTrue(duration.seconds <= 1.5,
                        "query is taking too long %f." % duration.seconds)
        self.assertEqual(len(results), testsuite_count*test_count*build_count)
