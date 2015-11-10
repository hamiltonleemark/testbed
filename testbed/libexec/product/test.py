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
from testdb.models import TestProduct
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

        args = parser.parse_args("product add product1 branch1".split())
        args.func(args)

        args = parser.parse_args("product add product1 branch2".split())
        args.func(args)

        products = api.filter("product1")
        self.assertEqual(products.count(), 2)
        branches = [str(item.branch) for item in products]
        self.assertTrue("branch1" in branches)
        self.assertTrue("branch2" in branches)

    def test_list_filter(self):
        """ Add a testsuite by context. """
        parser = TestsuiteTestCase.parser_create()

        cmd = "product add product2 branch1"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "product add product2 branch2"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "product add product3 branch2"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "product add product3 branch3"
        args = parser.parse_args(cmd.split())
        args.func(args)

        testsuites = TestProduct.filter(api.CONTEXT, "product3")
        branches = [str(item.branch) for item in testsuites]
        self.assertTrue(len(branches) == 2)
        self.assertTrue("branch2" in branches)
        self.assertTrue("branch3" in branches)

    def test_order1(self):
        """ Confirm order works. """

        parser = TestsuiteTestCase.parser_create()

        cmd = "product add product4 branch1 --order 1"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "product add product4 branch2 --order 2"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "product add product5 branch3 --order 3"
        args = parser.parse_args(cmd.split())
        args.func(args)

        products = TestProduct.filter(None, None)
        self.assertEqual(products.count(), 3)
        self.assertEqual(products[0].product.value, "product4")
        self.assertEqual(products[1].product.value, "product4")
        self.assertEqual(products[2].product.value, "product5")

    def test_order2(self):
        """ test_order2 Confirm order works. """

        parser = TestsuiteTestCase.parser_create()

        cmd = "product add product_order3 branch1 --order 3"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "product add product_order2 branch1 --order 1"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "product add product_order1 branch1 --order 1"
        args = parser.parse_args(cmd.split())
        args.func(args)

        products = TestProduct.filter(api.CONTEXT, "product_order")
        self.assertEqual(products.count(), 3)
        self.assertEqual(str(products[0].product), "product_order1")
        self.assertEqual(str(products[1].product), "product_order2")
        self.assertEqual(str(products[2].product), "product_order3")

    def test_order3(self):
        """ test_order3 Confirm order works. """

        parser = TestsuiteTestCase.parser_create()

        cmd = "product add product_order2 branch1 --order 2"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "product add product_order1 branch2 --order 1"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "product add product_order3 branch3 --order 3"
        args = parser.parse_args(cmd.split())
        args.func(args)

        products = TestProduct.filter(api.CONTEXT, "product_order")
        self.assertEqual(products.count(), 3)
        self.assertEqual(str(products[0].product), "product_order1")
        self.assertEqual(str(products[1].product), "product_order2")
        self.assertEqual(str(products[2].product), "product_order3")

    def test_add_testplan(self):
        """ test_add_testplan test add_testplan. """

        parser = TestsuiteTestCase.parser_create()

        cmd = "product add product1 branch1"
        args = parser.parse_args(cmd.split())
        args.func(args)

        cmd = "product testplan add product1 branch1 default"
        args = parser.parse_args(cmd.split())
        args.func(args)

        (product1, critem) = TestProduct.get_or_create("product.default",
                                                       "product1", "branch1")
        self.assertFalse(critem)
        self.assertTrue(product1)

        self.assertEqual(product1.key_get("testplan"), "default")
