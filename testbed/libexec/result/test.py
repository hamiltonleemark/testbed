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
import logging
from django.test import TestCase
from . import commands
from . import api
from testbed.libexec import build
from testbed.libexec import testsuite
from testbed.libexec import testplan


# pylint: disable=R0914
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

        start = datetime.datetime.now()
        for bitem in range(0, build_count):
            build.api.get_or_create("product1", "branch1", "build%d" % bitem)
            testkeys = [
                ("key1", "value1"),
                ("key2", "value2"),
                ("key3", "value3"),
                ("key4", "value4"),
                ("product", "product1"),
                ("branch", "branch1"),
                ("build", "build%d" % bitem)
            ]
            for titem in range(0, testsuite_count):
                testsuite.api.add_testsuite("default", "testsuite%d" % titem,
                                            testkeys)
                api.set_result("default", "product1", "branch1", "build1",
                               "testsuite%d" % titem, "test1", "pass",
                               testkeys)
        end = datetime.datetime.now()
        duration = end - start
        print "\ncreated testsuite %d %s" % (testsuite_count, duration)

        ##
        # Create testplan.
        start = datetime.datetime.now()
        for item in range(0, testsuite_count):
            testplan.api.get_or_create(testplan.api.CONTEXT,
                                       "testsuite%d" % item, item)
        end = datetime.datetime.now()
        duration = end - start
        print "testplan create %d %s" % (testsuite_count, duration)

        context = models.Context.objects.get(name=testplan.api.CONTEXT)
        testplan1 = models.Testplan.objects.get(context=context)
        orders = testplan1.testplanorder_set.all().order_by("order")
        self.assertEqual(len(orders), testsuite_count)

        results = api.list_result("default", [])
        self.assertEqual(len(results), build_count*testsuite_count)

        ##
        # Time retrieving testsuies.
        start = datetime.datetime.now()
        results = []
        for order in orders:
            testkeys = [
                ("key1", "value1"),
                ("key2", "value2"),
                ("key3", "value3"),
                ("key4", "value4"),
                ("product", "product1"),
                ("branch", "branch1"),
                ("build", "build1")
            ]
            results += testsuite.api.list_testsuite("default", testkeys,
                                                    order.testsuite.name)
        end = datetime.datetime.now()
        logging.info("testsuite search %d duration %d", testsuite_count,
                     duration)
        print "search testsuite count %d duration %s" % (testsuite_count,
                                                         duration)
        self.assertEqual(len(results), testsuite_count)

        start = datetime.datetime.now()
        results = []
        for order in orders:
            testkeys = [
                ("key1", "value1"),
                ("key2", "value2"),
                ("key3", "value3"),
                ("key4", "value4"),
                ("product", "product1"),
                ("branch", "branch1"),
                ("build", "build1")
            ]
            results += api.list_result("default", testkeys,
                                       order.testsuite.name)
        end = datetime.datetime.now()
        duration = end - start
        logging.info("search count %d duration %d", testsuite_count, duration)
        print "search test %d duration %s" % (testsuite_count, duration)
        self.assertEqual(len(results), testsuite_count)
