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

    def test_commands_add(self):
        """ Add a test. """
        count = 10

        build.api.get_or_create("product1", "branch1", "build1")

        testkeys = [("key1", "value1"), ("key2", "value2")]
        testsuite.api.add_testsuite("default", "testsuite1", testkeys)

        for item in range(0, count):
            api.set_result("default", "product1", "branch1", "build1",
                           "testsuite1", "test%d" % item, "pass", testkeys)

        testkeys += [("build", "build1"), ("product", "product1")]
        testkeys += [("branch", "branch1")]

        results = api.list_result("default", [])
        self.assertEqual(len(results), 10)

        start = datetime.datetime.now()
        results = api.list_result("default", testkeys)
        end = datetime.datetime.now()
        duration = end - start
        self.assertEqual(len(results), 10)

        logging.info("search count %d duration %d", count, duration)
        print "search count %d duration %s" % (count, duration)
