"""
Test test functionality.
"""
import argparse
from django.test import TestCase
from testdb.models import Testsuite
from testdb.models import Test
from . import commands


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
        """ Add a testsuite. """

        parser = TestTestCase.parser_create()

        args = parser.parse_args("test add testsuite1 test1".split())
        args.func(args)

        args = parser.parse_args("test add testsuite1 test2".split())
        args.func(args)

        names = [item.name.name for item in Testsuite.filter("testsuite1")]
        self.assertTrue(len(names)== 1)

        names = [item.name.name for item in Test.filter("testsuite1")]
        self.assertTrue(len(names)== 2)

        self.assertTrue(any("test1" in name for name in names))
        self.assertTrue(any("test2" in name for name in names))
