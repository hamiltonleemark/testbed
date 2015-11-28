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
CLI for associating a testplan to a product.
"""
import argparse
import logging
import yaml
from . import api


def do_add(args):
    """ Add a testsuite to the database. """

    return api.get_or_create(args.context, args.testsuite, args.order)


def do_change(args):
    """ Change the order of the testsuite in the testplan. """

    return api.change(args.context, args.testsuite, args.order)


def do_remove(args):
    """ Add a testsuite to the database. """

    return api.remove(args.context, args.order)


def do_pack(args):
    """ Pack testplan sequentially. """

    return api.pack(args.context)


# \todo args is missing
def do_list(args):
    """ List testsuites based on search criteria. """

    from testdb import models
    logging.info("listing testplan")

    testplans = models.Testplan.objects.all()
    root = {}
    for testplan in testplans:
        level = {}
        testkeys = [str(item.key)
                    for item in testplan.testplankeyset_set.all()]
        orders = []
        for plan in testplan.testplanorder_set.order_by("order"):
            testsuites = plan.testsuite_set.filter(context=testplan.context)
            if args.testsuite:
                testsuites = testsuites.filter(name__name=args.testsuite)

            for testsuite in testsuites:
                testsuitekeys = testsuite.testsuitekeyset_set.all()
                testsuitekeys = [str(item.testkey) for item in testsuitekeys]

                orders.append({
                    "name": str(testsuite.name_get()),
                    "order": plan.order,
                    "tests": [str(item.name_get())
                              for item in testsuite.test_set.all()],
                    "keys": testsuitekeys
                    })

        if testkeys:
            level["testkey"] = testkeys

        if orders:
            level["testsuites"] = orders
        root[str(testplan.context.name)] = level
    print yaml.dump(root, default_flow_style=False)


def do_add_key(args):
    """ Add test key and value to plan testsuite. """

    api.add_key(args.context, args.order, args.name, args.value)
    return True


def do_remove_key(args):
    """ Add a key to a testsuite. """

    api.remove_key(args.context, args.order, args.name)
    return True


def do_testplan_key_list(args):
    """ Add a key to a testsuite. """

    from testdb import models

    logging.info("list testplan keys")
    context = models.Testplan.context_get(args.context)
    (testplan, _) = models.Testplan.get(context=context)
    testkeys = testplan.testplankeyset_set.filter(args.filter).order_by("key")
    for testkey in testkeys:
        print testkey


def do_add_test(args):
    """ Add a test to a testplan. """

    from testdb import models

    ##
    # Make sure testsuite is part of the test plan.
    try:
        context = models.Testplan.context_get(args.context)
        testplan = models.Testplan.objects.get(context=context)
    except (models.Context.DoesNotExist, models.Testplan.DoesNotExist):
        raise ValueError("testplan with context %s missing" % args.context)

    try:
        planorder = testplan.testplanorder_set.get(order=args.order,
                                                   testplan=testplan)
        testsuite = models.Testsuite.objects.get(context=context,
                                                 testplanorder=planorder)
    except (models.Testsuite.DoesNotExist, models.TestplanOrder.DoesNotExist):
        raise ValueError("testplan %s does not contain %s" % (args.context,
                                                              args.order))

    models.Test.get_or_create(testsuite, args.name, "pass", [])
    logging.info("add test %s to testsuite %s.%s", args.name, planorder.order,
                 testsuite.name)
    return True


def do_test_remove(args):
    """ Remove a test from a testplan. """

    from testdb import models

    ##
    # Make sure testsuite is part of the test plan.
    try:
        context = models.Testplan.context_get(args.context)
        testplan = models.Testplan.objects.get(context=context)
    except (models.Context.DoesNotExist, models.Testplan.DoesNotExist):
        raise ValueError("testplan with context %s missing" % args.context)

    try:
        planorder = testplan.testplanorder_set.get(order=args.order,
                                                   testplan=testplan)
        testsuite = models.Testsuite.objects.get(context=context,
                                                 testplanorder=planorder)
    except (models.Testsuite.DoesNotExist, models.TestplanOrder.DoesNotExist):
        raise ValueError("testplan %s does not contain %s" % (args.context,
                                                              args.order))

    test = testsuite.test_set.get(name__name=args.name)
    test.delete()
    logging.info("removing test %s from testsuite %s.%s", args.name,
                 planorder.order, testsuite.name)
    return True


def valid_order(value):
    """ Make sure order is either a positive number of special value of all."""

    if value == "all":
        return value

    ivalue = int(value)
    if ivalue < 0:
        raise argparse.ArgumentTypeError("%s is not all or positive integer",
                                         value)
    return value


def add_subparser(subparser):
    """ Create testsuite CLI commands. """

    parser = subparser.add_parser("testplan",
                                  help="Setup and modify test plans.",
                                  description=__doc__)
    parser.add_argument("--context", default=api.CONTEXT, type=str,
                        help="Specify a different context.")
    rootparser = parser.add_subparsers()

    ##
    # Add
    parser = rootparser.add_parser(
        "add", description="Add a testsuite to the testplan",
        help="Add a testsuite.")
    parser.set_defaults(func=do_add)
    parser.add_argument("testsuite", type=str, help="Name of the testsuite.")
    parser.add_argument("--order", type=int, default=-1,
                        help="Order of testsuite as viewed on the website."
                        "If not specified the next sequential value is "
                        "assumed")

    ##
    # Change
    parser = rootparser.add_parser(
        "change", description="Change testplan",
        help="Add a testsuite.")
    parser.set_defaults(func=do_change)
    parser.add_argument("testsuite", type=str, help="Name of the testsuite.")
    parser.add_argument("order", type=int,
                        help="Change the order of the testsuite.")

    ##
    # Remove
    parser = rootparser.add_parser(
        "remove", description="Remove a testsuite from the testplan",
        help="Remove a testsuite.")
    parser.set_defaults(func=do_remove)
    parser.add_argument("order", type=int, help="Remove plan based on order.")

    ##
    # List
    parser = rootparser.add_parser("list",
                                   description="List all of the testsuites.",
                                   help="List testsuite.")
    parser.set_defaults(func=do_list)
    parser.add_argument("--testsuite", help="Filter testsuite")

    ##
    # Pack
    parser = rootparser.add_parser(
        "pack", description="Pack testplan into sequential list",
        help="Pack test plan.")
    parser.set_defaults(func=do_pack)

    ##
    # Key
    parser = rootparser.add_parser("key",
                                   description="Modify keys testplan.",
                                   help="Modify testplan keys.")
    subparser = parser.add_subparsers()
    parser = subparser.add_parser("add",
                                  description="Add key and value to testplan",
                                  help="Add key and value to testplan.")

    parser.set_defaults(func=do_add_key)
    parser.add_argument("order", type=valid_order,
                        help="Order of testsuite as viewed on the website.")
    parser.add_argument("name", type=str, help="Name of the key to add")
    parser.add_argument("value", type=str, help="Key's value")

    parser = subparser.add_parser("remove",
                                  description="Remove a testsuite key",
                                  help="Add a testsuite key")
    parser.set_defaults(func=do_remove_key)
    parser.add_argument("order", type=valid_order,
                        help="Order of testsuite as viewed on the website.")
    parser.add_argument("name", type=str, help="Name of the key")

    #
    ##

    ##
    # Test CLI
    parser = rootparser.add_parser("test",
                                   description="Modify tests in testsuite.",
                                   help="Modify test in testsuite.")
    subparser = parser.add_subparsers()
    tparser = subparser.add_parser("add", description="Add key",
                                   help="add test.")

    tparser.set_defaults(func=do_add_test)
    tparser.add_argument("order", type=valid_order, help="testsuite name")
    tparser.add_argument("name", type=str, help="name of test")

    tparser = subparser.add_parser("remove", description="Add key",
                                   help="add test.")
    tparser.set_defaults(func=do_test_remove)
    tparser.add_argument("order", type=valid_order, help="testsuite name")
    tparser.add_argument("name", type=str, help="name of test")
    #
    ##

    return subparser
