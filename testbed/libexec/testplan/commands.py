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
import logging
import yaml
from . import api


def do_testsuite_add(args):
    """ Add a testsuite to the database. """

    return api.get_or_create(args.context, args.testsuite, args.order)


def do_testsuite_remove(args):
    """ Add a testsuite to the database. """

    return api.remove(args.context, args.testsuite)


def do_testplan_list(args):
    """ List testsuites based on search criteria. """

    from testdb import models
    logging.info("listing testplan")

    testplans = models.Testplan.objects.all()
    root = {}
    for testplan in testplans:
        level = {}
        testkeys = {str(item.testkey.key): str(item.testkey.value)
                    for item in testplan.testplankeyset_set.all()}

        testsuites = [{item.order: str(item.testsuite.name),
                       "tests": [str(item)
                                 for item in item.testsuite.test_set.all()]}
                      for item in testplan.testplanorder_set.order_by("order")]

        if testkeys:
            level["testkey"] = testkeys
        if testsuites:
            level["testsuites"] = testsuites
        root[args.context] = level
    print yaml.dump(root, default_flow_style=False)


def do_testplan_key_add(args):
    """ Add a key to a testsuite. """

    from testdb import models
    logging.info("add testpan key %s", args.name)

    (testkey, _) = models.TestKey.get_or_create(key=args.name,
                                                value=args.value)

    (context, _) = models.Context.objects.get_or_create(name=args.context)
    (testplan, _) = models.Testplan.objects.get_or_create(context=context)
    testplan.testplankeyset_set.get_or_create(testplan=testplan,
                                              testkey=testkey)


def do_testplan_key_remove(args):
    """ Add a key to a testsuite. """

    from testdb import models
    logging.info("remove key %s from testpan %s", args.key, args.context)
    context = models.Context.objects.get_or_create(name=args.context)
    (testplan, _) = models.Testplan.get(testsuite__context=context)
    testkey = testplan.testplankeyset_set.get(testkey__key=args.key)
    testkey.delete()


def do_testplan_key_list(args):
    """ Add a key to a testsuite. """

    from testdb import models

    logging.info("list testplan keys")
    (testplan, _) = models.Testplan.get(context=args.context)
    testkeys = testplan.testplankeyset_set.filter(args.filter).order_by("key")
    for testkey in testkeys:
        print testkey


def do_testplan_test_add(args):
    """ Add a test to a testplan. """

    from testdb import models
    logging.info("add test to testplan tstsuite key %s", args.name)

    ##
    # Make sure testsuite is part of the test plan.
    (context, _) = models.Context.objects.get_or_create(name=args.context)
    try:
        testplan = models.Testplan.objects.get(context=context)
    except models.Context.DoesNotExist:
        raise ValueError("testplan %s does not exist", args.context)

    try:
        (name, _) = models.TestsuiteName.objects.get_or_create(
            name=args.testsuite)
        testsuite = models.Testsuite.objects.get(name=name)
    except models.Testsuite.DoesNotExist:
        raise ValueError("testuite %s does not exist", args.testsuite)

    try:
        models.TestplanOrder.objects.get(testsuite=testsuite,
                                         testplan=testplan)
    except models.TestplanOrder.DoesNotExist:
        raise ValueError("testplan %s does not contain testsuite %s",
                         args.context, args.testsuite)
    return models.Test.get_or_create(testsuite, args.name, [])


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
        "add",
        description="Add a testsuite to the testplan",
        help="Add a testsuite.")
    parser.set_defaults(func=do_testsuite_add)
    parser.add_argument("testsuite", type=str, help="Name of the testsuite.")
    parser.add_argument("--order", type=int, default=-1,
                        help="Order of testsuite as viewed on the website."
                        "If not specified the next sequential value is "
                        "assumed")

    ##
    # Remove
    parser = rootparser.add_parser(
        "remove",
        description="Remove a testsuite from the testplan",
        help="Remove a testsuite.")
    parser.set_defaults(func=do_testsuite_remove)
    parser.add_argument("testsuite", type=str, help="Name of the testsuite.")

    ##
    # List
    parser = rootparser.add_parser("list",
                                   description="List all of the testsuites.",
                                   help="List testsuite.")
    parser.set_defaults(func=do_testplan_list)
    parser.add_argument("--filter", type=str, help="Filter testsuites")

    ##
    # Key
    parser = rootparser.add_parser("key",
                                   description="Modify keys testplan.",
                                   help="Modify testplan keys.")
    subparser = parser.add_subparsers()
    parser = subparser.add_parser("add", description="Add key",
                                  help="add test.")

    parser.set_defaults(func=do_testplan_key_add)
    parser.add_argument("name", type=str, help="Name of the key")
    parser.add_argument("value", type=str, help="Key's value")
    parser.add_argument(
        "--strict", default=False, action="store_true",
        help="A key which must strictly match an existing values")

    parser = subparser.add_parser("remove",
                                  description="Add a testsuite key",
                                  help="Add a testsuite key")
    parser.add_argument("name", type=str, help="Name of the key")
    parser.add_argument("--value", type=str, help="Key's value")
    parser.set_defaults(func=do_testplan_key_remove)

    ##
    # Test
    parser = rootparser.add_parser("test",
                                   description="Modify tests in testsuite.",
                                   help="Modify test in testsuite.")
    subparser = parser.add_subparsers()
    parser = subparser.add_parser("add", description="Add key",
                                  help="add test.")

    parser.set_defaults(func=do_testplan_test_add)
    parser.add_argument("testsuite", type=str, help="testsuite name")
    parser.add_argument("name", type=str, help="name of test")

    return subparser
