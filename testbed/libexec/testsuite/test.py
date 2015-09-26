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
from testdb.models import Testplan
from . import commands
from testbed.libexec import testplan


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

        testplan.api.get_or_create(testplan.api.CONTEXT, "bob",
                                   testplan.api.ORDER_NEXT)
        testplan.api.get_or_create(testplan.api.CONTEXT, "mark",
                                   testplan.api.ORDER_NEXT)
        args = parser.parse_args("testsuite add bob".split())
        args.func(args)

        args = parser.parse_args("testsuite add mark".split())
        args.func(args)

        names = [item.name.name for item in Testsuite.objects.all()]
        self.assertTrue("bob" in names)
        self.assertTrue("mark" in names)

        context = [item.context.name for item in Testsuite.objects.all()]
        self.assertTrue("default" in context)

    def test_context_add(self):
        """ Add a testsuite by context. """
        parser = TestsuiteTestCase.parser_create()

        testplan.api.get_or_create(testplan.api.CONTEXT, "testsuite1",
                                   testplan.api.ORDER_NEXT)

        cmd = "testsuite --context testplan add testsuite1"
        args = parser.parse_args(cmd.split())
        args.func(args)

        names = [item.name.name for item in Testsuite.objects.all()]
        self.assertTrue("testsuite1" in names)
        context = [item.context.name for item in Testsuite.objects.all()]
        self.assertTrue("testplan" in context)

    def test_list_filter(self):
        """ Add a testsuite by context. """
        parser = TestsuiteTestCase.parser_create()

        testplan.api.get_or_create(testplan.api.CONTEXT, "testsuite_bob1",
                                   testplan.api.ORDER_NEXT)
        testplan.api.get_or_create(testplan.api.CONTEXT, "testsuite_bob2",
                                   testplan.api.ORDER_NEXT)
        testplan.api.get_or_create(testplan.api.CONTEXT, "testsuite_ken1",
                                   testplan.api.ORDER_NEXT)

        cmd = "testsuite add testsuite_bob1"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testsuite add testsuite_bob2"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testsuite add testsuite_ken1"
        args = parser.parse_args(cmd.split())
        args.func(args)

        testsuites = Testsuite.contains("default", "testsuite_bob1")
        items = [item for item in testsuites]
        self.assertTrue(len(items) == 1)
        names = [item.name.name for item in items]
        self.assertTrue(any("bob1" in name for name in names))
        self.assertTrue(any("bob2" in name for name in names))
