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
import api

def testsuite_add(args):
    """ Add a testsuite to the database. """

    from testdb import models

    print "MARK: bob"
    return api.get_or_create(args.context, args.testsuite, args.order)
    


def test_add(args):
    """ Add a testsuite to the database. """

    from testdb import models

    logging.info("adding testsuite to testplan %s", args.testsuite)
    (testsuite, _) = api.get_or_create(args.context, args.testsuite, -1)
    (name, _) = models.TestName.objects.get_or_create(name=args.name)
    models.Test.objects.get_or_create(testsuite=testsuite, name=name)


def testsuite_list(args):
    """ List testsuites based on search criteria. """

    from testdb import models
    logging.info("listing testsuites")

    testsuites = models.Testsuite.filter(args.filter)

    datatree = testbed.core.config.DataTree()

    for testsuite in testsuites:
        testkeys = [str(item.testkey)
                    for item in testsuite.testsuitekeyset_set.all()]
        tests = [str(item) for item in testsuite.test_set.all()]

        root = {}
        if tests:
            root["tests"] = tests
        if testkeys:
            root["testkey"] = testkeys

        key = [str(testsuite.context), "testsuite.%s" % testsuite.name]
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

    (testsuite, _) = models.Testsuite.get_or_create(args.context,
                                                    args.testsuite)
    testsuite.testsuitekeyset_set.get_or_create(testkey=testkey)


def key_list(args):
    """ Add a key to a testsuite. """

    from testdb import models

    LOGGER.info("list test keys")
    testkeys = models.TestKey.filter(args.filter).order_by("key")
    for testkey in testkeys:
        print testkey


def add_subparser(subparser):
    """ Create testsuite CLI commands. """

    parser = subparser.add_parser("testplan", help=__doc__)
    parser.add_argument("--context", default="testplan.default", type=str,
                        help="Specify a different context.")
    subparser = parser.add_subparsers()

    ##
    # Add
    parser = subparser.add_parser(
        "add",
        description="Add a testsuite to the testplan",
        help="Add a testsuite.")
    parser.set_defaults(func=testsuite_add)
    parser.add_argument("testsuite", type=str, help="Name of the testsuite.")
    parser.add_argument("--order", type=int, default=-1,
                        help="Order of testsuite as viewed on the website."
                        "If not specified the next sequential value is "
                        "assumed")

    ##
    # List
    parser = subparser.add_parser("list",
                                  description="List all of the testsuites.",
                                  help="List testsuite")
    parser.set_defaults(func=testsuite_list)
    parser.add_argument("--filter", type=str, help="Filter testsuites")

    ##
    # Test 
    parser = subparser.add_parser("test",
                                  description="modify test for the testsuite",
                                  help="Modify test information.")
    subparser = parser.add_subparsers()
    parser = subparser.add_parser("add", description="Add test",
                                  help="add test.")

    parser.set_defaults(func=test_add)
    parser.add_argument("testsuite", type=str, help="Name of the testsuite.")
    parser.add_argument("name", type=str, help="Name of the test.")

    ##
    # CLI for adding testsuite keys
    # Keys are how testsuites are organized and searched in the database.
    parser = subparser.add_parser("key",
                                  help="APIs for manipulating testsuite keys")
    subparser = parser.add_subparsers()
    parser = subparser.add_parser(
        "create",
        description="CLI for creating testsuite keys",
        help="Create a testsuite key.")
    parser.add_argument("name", type=str, help="Name of the key.")
    parser.add_argument(
        "--strict", default=False, action="store_true",
        help="Testsuite key values must strictly match an existing value "
             "otherwise any new values will be acceptabed")
    parser.set_defaults(func=key_create)

    parser = subparser.add_parser("add",
                                  description="Add a testsuite key",
                                  help="Add a testsuite key")
    parser.add_argument("testsuite", type=str, help="Testsuite name")
    parser.add_argument("key", type=str, help="Name of the key")
    parser.add_argument("value", type=str, help="Key's value")
    parser.add_argument("--order", type=int, help="testuite order for viewing")
    parser.set_defaults(func=key_add)

    ##
    # List
    parser = subparser.add_parser("list", description="List test keys",
                                  help="List testsuite")
    parser.add_argument("--filter", type=str, help="Filter test keys")
    parser.set_defaults(func=key_list)

    ##
    # List
    return subparser
