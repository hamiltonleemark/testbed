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
Test testsuite functionality.
"""
import argparse
from django.test import TestCase
from testdb.models import Testsuite
from testdb.models import TestplanOrder
from . import commands


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

        args = parser.parse_args("testplan add bob".split())
        args.func(args)

        args = parser.parse_args("testplan test add bob ken".split())
        args.func(args)

        args = parser.parse_args("testplan add mark".split())
        args.func(args)

        args = parser.parse_args("testplan test add mark ken".split())
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

        cmd = "testplan --context testplan test add testsuite1 test1"
        args = parser.parse_args(cmd.split())
        args.func(args)

        names = [item.name.name for item in Testsuite.objects.all()]
        self.assertTrue("testsuite1" in names)
        context = [item.context.name for item in Testsuite.objects.all()]
        self.assertTrue(any("testplan" in item for item in context))

    def test_list_filter(self):
        """ Add a testsuite by context. """
        parser = TestsuiteTestCase.parser_create()

        cmd = "testplan --context testplan1 add testsuite_bob1"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testplan --context testplan1 test add testsuite_bob1 test2"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testplan --context testplan2 add testsuite_bob2"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testplan --context testplan2 test add testsuite_bob2 test3"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testplan --context testplan2 add testsuite_ken1"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testplan --context testplan2 test add testsuite_ken1 test4"
        args = parser.parse_args(cmd.split())
        args.func(args)

        testsuites = Testsuite.objects.filter(context__name="testplan2")
        names = [item.name.name for item in testsuites]
        self.assertTrue(len(names) == 2)
        self.assertTrue(any("bob2" in name for name in names))
        self.assertTrue(any("ken1" in name for name in names))

    def test_order1(self):
        """ Confirm order works. """

        parser = TestsuiteTestCase.parser_create()

        cmd = "testplan add testsuite_order1 --order 1"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testplan add testsuite_order2 --order 2"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testplan add testsuite_order3 --order 3"
        args = parser.parse_args(cmd.split())
        args.func(args)

        testplans = TestplanOrder.objects.all().order_by("order")
        self.assertEqual(testplans.count(), 3)
        self.assertEqual(testplans[0].testsuite.name.name, "testsuite_order1")
        self.assertEqual(testplans[1].testsuite.name.name, "testsuite_order2")
        self.assertEqual(testplans[2].testsuite.name.name, "testsuite_order3")

    def test_order2(self):
        """ test_order2 Confirm order works. """

        parser = TestsuiteTestCase.parser_create()

        cmd = "testplan add testsuite_order3 --order 3"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testplan add testsuite_order2 --order 1"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testplan add testsuite_order1 --order 1"
        args = parser.parse_args(cmd.split())
        args.func(args)

        testplans = TestplanOrder.objects.all().order_by("order")
        self.assertEqual(testplans.count(), 3)
        self.assertEqual(testplans[0].testsuite.name.name, "testsuite_order1")
        self.assertEqual(testplans[1].testsuite.name.name, "testsuite_order2")
        self.assertEqual(testplans[2].testsuite.name.name, "testsuite_order3")

    def test_order3(self):
        """ test_order2 Confirm order works. """

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

        testplans = TestplanOrder.objects.all().order_by("order")
        self.assertEqual(testplans.count(), 3)
        self.assertEqual(testplans[0].testsuite.name.name, "testsuite_order1")
        self.assertEqual(testplans[1].testsuite.name.name, "testsuite_order2")
        self.assertEqual(testplans[2].testsuite.name.name, "testsuite_order3")

    def test_order_one(self):
        """ test_order_one Confirm order works. """

        parser = TestsuiteTestCase.parser_create()

        cmd = "testplan add testsuite_order_one"
        args = parser.parse_args(cmd.split())
        args.func(args)

        testplans = TestplanOrder.objects.all()
        self.assertEqual(testplans.count(), 1)
        self.assertEqual(testplans[0].order, 1)

        cmd = "testplan add testsuite_order_one --order 2"
        args = parser.parse_args(cmd.split())
        args.func(args)
        testplans = TestplanOrder.objects.all()
        self.assertEqual(testplans.count(), 1)
        self.assertEqual(testplans[0].order, 2)
