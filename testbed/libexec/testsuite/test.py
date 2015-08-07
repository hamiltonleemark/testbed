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

        cmd = "testsuite --context testplan1 add testsuite_bob1"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testsuite --context testplan2 add testsuite_bob2"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "testsuite --context testplan2 add testsuite_ken1"
        args = parser.parse_args(cmd.split())
        args.func(args)

        testsuites = Testsuite.filter("bob")
        items = [item for item in testsuites]
        self.assertTrue(len(items) == 2)
        names = [item.name.name for item in items]
        self.assertTrue(any("bob1" in name for name in names))
        self.assertTrue(any("bob2" in name for name in names))

        testsuites = Testsuite.filter("testplan2")
        names = [item.name.name for item in testsuites]
        self.assertTrue(len(names) == 2)
        self.assertTrue(any("bob2" in name for name in names))
        self.assertTrue(any("ken1" in name for name in names))
