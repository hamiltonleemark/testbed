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
CLI for creating testplan.
"""
import logging
import yaml
import testbed.core.config
from . import api


def product_add(args):
    """ Add a product to the database. """
    return api.get_or_create(args.name, args.branch, args.order)


def testplan_add(args):
    """ Add a testplan to the database. """

    from testdb import models

    logging.info("adding testplan to product %s", args.testplan)
    (testplan, _) = api.get_or_create(api.CONTEXT, args.name, -1)
    (name, _) = models.TestName.objects.get_or_create(name=args.name)
    testsuite = testplan.testsuite
    models.Test.objects.get_or_create(testsuite=testsuite, name=name)


def product_list(args):
    """ List products based on search criteria. """

    from testdb import models
    logging.info("listing products")

    testplans = models.Testplan.filter(args.filter)

    datatree = testbed.core.config.DataTree()

    for testplan in testplans:
        testsuite = testplan.testsuite
        testkeys = [str(item.testkey)
                    for item in testsuite.testsuitekeyset_set.all()]
        tests = [str(item) for item in testsuite.test_set.all()]

        root = {}
        if tests:
            root["tests"] = tests
        if testkeys:
            root["testkey"] = testkeys

        key = [api.CONTEXT, "testsuite.%s" % testsuite.name]
        datatree.add(key, root)
    print yaml.dump(datatree)


def key_create(args):
    """ Add a key to a testsuite. """

    from testdb import models

    logging.info("create testsuite key %s", args.name)
    models.Key.objects.get_or_create(value=args.name)


def key_add(args):
    """ Add a key to a testsuite. """

    from testdb import models

    logging.info("add value to testsuite key %s", args.key)
    (testkey, _) = models.TestKey.get_or_create(key=args.key, value=args.value)

    (testsuite, _) = models.Testsuite.get_or_create(api.CONTEXT,
                                                    args.testsuite)
    testsuite.testsuitekeyset_set.get_or_create(testkey=testkey)


def key_list(args):
    """ Add a key to a testsuite. """

    from testdb import models

    logging.info("list test keys")
    testkeys = models.TestKey.filter(args.filter).order_by("key")
    for testkey in testkeys:
        print testkey


def add_subparser(subparser):
    """ Create testsuite CLI commands. """

    parser = subparser.add_parser("product", help=__doc__)
    subparser = parser.add_subparsers()

    ##
    # Add
    parser = subparser.add_parser("add",
                                  description="Add a product to the database",
                                  help="Add a product.")
    parser.set_defaults(func=product_add)
    parser.add_argument("name", type=str, help="Name of the product.")
    parser.add_argument("branch", type=str, help="Branch name of the product.")
    parser.add_argument("--order", type=int, default=-1,
                        help="Order of product as viewed on the website."
                        "If not specified the next sequential value is "
                        "assumed")

    ##
    # List
    parser = subparser.add_parser("list",
                                  description="List all of the products.",
                                  help="List products")
    parser.set_defaults(func=product_list)
    parser.add_argument("--filter", type=str, help="Filter products")

    ##
    # Add testplan
    parser = subparser.add_parser(
        "testplan",
        description="modify testplan for the product",
        help="Modify test information.")
    subparser = parser.add_subparsers()
    parser = subparser.add_parser("add", description="Add testplan",
                                  help="add test.")

    parser.set_defaults(func=testplan_add)
    parser.add_argument("name", type=str, help="Name of testplan.")

    return subparser
