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
CLI for tests.
"""
import logging
import yaml
import argparse
from . import api
from testbed.core import config

LOGGER = logging.getLogger(__name__)


def valid_testkey(value):
    """ Make sure order is either a positive number of special value of all."""

    return value.split("=")


def do_set(args):
    """ Add a test. """

    api.set_result(args.context, args.product, args.branch, args.build,
                   args.testsuite, args.test, args.result, args.testkeys)


def do_list_result(args):
    """ List testsuites based on search criteria. """

    LOGGER.info("listing tests")

    tests = api.list_result(args.context, args.product, args.branch, [],
                            args.build)

    data = config.DataTree()
    for test in tests:
        product = test.key_get("product")
        branch = test.key_get("branch")
        build = test.key_get("build")

        key = "%s.%s" % (str(product), str(branch))
        testsuite_name = str(test.testsuite.name)

        if test.status == 0:
            result = "pass"
        elif test.status == 1:
            result = "fail"

        data.add([args.context, key, str(build), testsuite_name,
                  str(test.name)], result)

    print yaml.dump(data.root, default_flow_style=False)


def add_subparser(subparser):
    """ Create testsuite CLI commands. """

    ##
    # Adding a test requires a testsuite.
    #
    # test add <testsuite> <name>
    parser = subparser.add_parser("result", help=__doc__)
    parser.add_argument("--context", default="default", type=str,
                        help="Testsuite context.")
    subparser = parser.add_subparsers()

    parser = subparser.add_parser("set", help="set test result",
                                  description="set test result")
    parser.set_defaults(func=do_set)
    parser.add_argument("product", type=str, help="Name of product.")
    parser.add_argument("branch", type=str, help="Product branch name.")
    parser.add_argument("build", type=str, help="build.")
    parser.add_argument("testsuite", type=str, help="Testsuite name.")
    parser.add_argument("test", type=str, help="test name")
    parser.add_argument("result", default=None, choices=["pass", "fail"],
                        help="Specify result for a test.")
    parser.add_argument("testkeys", default=[], nargs=argparse.REMAINDER,
                        type=valid_testkey, help="Specify result for a test.")

    parser = subparser.add_parser("list",
                                  description="List tests in their testsuit.",
                                  help="List test.")
    parser.add_argument("product", type=str, help="Name of product.")
    parser.add_argument("branch", type=str, help="Product branch name.")
    parser.add_argument("--build", type=str, help="build.")
    parser.set_defaults(func=do_list_result)
    return subparser
