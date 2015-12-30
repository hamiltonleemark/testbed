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
Test testsuite functionality.
"""
import argparse
from django.test import TestCase
from testdb.models import Testsuite
from testdb.models import TestplanOrder
from testdb.models import Testplan
from . import commands
from . import api


class TestsuiteTestCase(TestCase):
    """ Tests for Django backend.
    These test must derive from django.test.TestCase. """

    @staticmethod
    def parser_create():
        """ Create sub parser. """
        arg_parser = argparse.ArgumentParser(prog="tbd")
        subparser = arg_parser.add_subparsers(title="subcommands")
        commands.add_subparser(subparser)
        return arg_parser

    def test_commands_add(self):
        """ Add a testsuite. """

        parser = TestsuiteTestCase.parser_create()

        args = parser.parse_args("testplan add bob --order 0".split())
        args.func(args)

        args = parser.parse_args("testplan test add 0 ken".split())
        args.func(args)

        args = parser.parse_args("testplan add mark --order 1".split())
        args.func(args)

        args = parser.parse_args("testplan test add 1 ken".split())
        args.func(args)

        names = [item.name.name for item in Testsuite.objects.all()]
        self.assertTrue("bob" in names)
        self.assertTrue("mark" in names)

        context = [item.context.name for item in Testsuite.objects.all()]
        self.assertTrue("testplan.default" in context)

    def test_context_add(self):
        """ Add a testsuite by context. """
        parser = TestsuiteTestCase.parser_create()

        cmd = "testplan --context testplan add testsuite1"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testplan --context testplan test add 0 test1"
        args = parser.parse_args(cmd.split())
        args.func(args)

        names = [item.name.name for item in Testsuite.objects.all()]
        self.assertTrue("testsuite1" in names)

        context = [item.context.name for item in Testsuite.objects.all()]
        self.assertTrue(any("testplan" in item for item in context))

    def atest_list_filter(self):
        """ Add a testsuite by context. """
        parser = TestsuiteTestCase.parser_create()

        cmd = "testplan --context testplan1 add testsuite_bob1 --order 0"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testplan --context testplan1 test add 0 test2"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testplan --context testplan2 add testsuite_bob2 --order 1"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testplan --context testplan2 test add 1 test3"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testplan --context testplan2 add testsuite_ken1 --order 2"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testplan --context testplan2 test add 2 test4"
        args = parser.parse_args(cmd.split())
        args.func(args)

        context = Testplan.context_get("testplan2")
        testsuites = Testsuite.objects.filter(context=context)
        names = [item.name.name for item in testsuites]
        self.assertTrue(len(names) == 2)
        self.assertTrue(any("bob2" in name for name in names))
        self.assertTrue(any("ken1" in name for name in names))

    def test_pack(self):
        """ Pack content. """

        parser = TestsuiteTestCase.parser_create()

        cmd = "testplan add testsuite_order1 --order 10"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testplan add testsuite_order2 --order 11"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testplan add testsuite_order3 --order 12"
        args = parser.parse_args(cmd.split())
        args.func(args)

        testplan1 = api.get(api.CONTEXT, [])
        orders = [item for item in testplan1.testsuites_all()]
        self.assertEqual(len(orders), 3)

        self.assertEqual(orders[0][1].name.name, "testsuite_order1")
        self.assertEqual(orders[1][1].name.name, "testsuite_order2")
        self.assertEqual(orders[2][1].name.name, "testsuite_order3")

        cmd = "testplan pack"
        args = parser.parse_args(cmd.split())
        args.func(args)
        self.assertEqual(len(orders), 3)

        testplan1 = api.get(api.CONTEXT, [])
        orders = [item for item in testplan1.testsuites_all()]
        self.assertEqual(orders[0][0], 0)
        self.assertEqual(orders[1][0], 1)
        self.assertEqual(orders[2][0], 2)

        self.assertEqual(orders[0][1].name.name, "testsuite_order1")
        self.assertEqual(orders[1][1].name.name, "testsuite_order2",
                         "%s != testsuite_order2" % orders[1][1].name.name)
        self.assertEqual(orders[2][1].name.name, "testsuite_order3")

    def test_order1(self):
        """ Confirm order works. """

        parser = TestsuiteTestCase.parser_create()

        cmd = "testplan add testsuite_order1 --order 0"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testplan add testsuite_order2 --order 1"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testplan add testsuite_order3 --order 2"
        args = parser.parse_args(cmd.split())
        args.func(args)

        testplan1 = api.get(api.CONTEXT, [])
        orders = [item for item in testplan1.testsuites_all()]
        self.assertEqual(len(orders), 3)

        self.assertEqual(orders[0][1].name.name, "testsuite_order1")
        self.assertEqual(orders[1][1].name.name, "testsuite_order2")
        self.assertEqual(orders[2][1].name.name, "testsuite_order3")

    def test_order2(self):
        """ test_order2 Confirm order works. """

        parser = TestsuiteTestCase.parser_create()

        cmd = "testplan add testsuite_order3 --order 2"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testplan add testsuite_order2 --order 0"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testplan add testsuite_order1 --order 0"
        args = parser.parse_args(cmd.split())
        args.func(args)

        testplan1 = api.get(api.CONTEXT, [])
        orders = [item for item in testplan1.testsuites_all()]

        self.assertEqual(len(orders), 3)
        self.assertEqual(orders[0][1].name.name, "testsuite_order1")
        self.assertEqual(orders[1][1].name.name, "testsuite_order2")
        self.assertEqual(orders[2][1].name.name, "testsuite_order3")

    def test_order3(self):
        """ test_order3 Confirm order works. """

        parser = TestsuiteTestCase.parser_create()

        cmd = "testplan add testsuite_order2 --order 2"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testplan add testsuite_order1 --order 1"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testplan add testsuite_order3 --order 3"
        args = parser.parse_args(cmd.split())
        args.func(args)

        testplan1 = api.get(api.CONTEXT, [])
        orders = [item for item in testplan1.testsuites_all()]
        TestplanOrder.objects.all().order_by("order")

        self.assertEqual(len(orders), 3)
        self.assertEqual(orders[0][1].name.name, "testsuite_order1")
        self.assertEqual(orders[1][1].name.name, "testsuite_order2",
                         "%s != testsuite_order2" % orders[1][1].name.name)
        self.assertEqual(orders[2][1].name.name, "testsuite_order3")

        cmd = "testplan pack"
        args = parser.parse_args(cmd.split())
        args.func(args)
        self.assertEqual(len(orders), 3)
        self.assertEqual(orders[0][1].name.name, "testsuite_order1")
        self.assertEqual(orders[1][1].name.name, "testsuite_order2",
                         "%s != testsuite_order2" % orders[1][1].name.name)
        self.assertEqual(orders[2][1].name.name, "testsuite_order3")

    def test_order_one(self):
        """ test_order_one Confirm order works. """
        parser = TestsuiteTestCase.parser_create()

        cmd = "testplan add testsuite_order_one"
        args = parser.parse_args(cmd.split())
        args.func(args)

        testplans = TestplanOrder.objects.all()
        self.assertEqual(testplans.count(), 1)
        self.assertEqual(testplans[0].order, api.ORDER_FIRST,
                         "order %s != %s is wrong" % (testplans[0].order,
                                                      api.ORDER_FIRST))

        ##
        # Now change the order
        cmd = "testplan change testsuite_order_one 2"
        args = parser.parse_args(cmd.split())
        args.func(args)
        testplans = TestplanOrder.objects.all()

        self.assertEqual(testplans.count(), 1)
        self.assertEqual(testplans[0].order, 2,
                         "first order %s == %s" % (testplans[0].order, 2))

        cmd = "testplan pack"
        args = parser.parse_args(cmd.split())
        args.func(args)
        testplans = TestplanOrder.objects.all()
        self.assertEqual(testplans.count(), 1)
        self.assertEqual(testplans[0].order, api.ORDER_FIRST)

    def test_inorder(self):
        """ test_in_order. Insert testsuites in order."""
        testsuite_count = 2

        for item in range(0, testsuite_count):
            testsuite_name = "testsuite%d" % item
            (_, _, created) = api.get_or_create("default", testsuite_name,
                                                item)
            self.assertTrue(created, "created testsuite%d" % item)

        testplan1 = api.get("default", [])
        orders = [item for item in testplan1.testsuites_all()]
        self.assertEqual(len(orders), testsuite_count, "missing testsuite")
        for (order, testsuite) in orders:
            expected_name = "testsuite%d" % order
            self.assertEqual(expected_name, testsuite.name.name,
                             "testsuite names do not match")

    # pylint: disable=R0201
    def test_testplan_simple(self):
        """ Add testsuite and tests to the testsuites. """

        parser = TestsuiteTestCase.parser_create()

        cmd = "testplan add testsuite1"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testplan add testsuite2"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testplan test add 0 test1"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testplan test add 0 test2"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testplan test add 1 test2"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testplan test add 1 test3"
        args = parser.parse_args(cmd.split())
        args.func(args)
