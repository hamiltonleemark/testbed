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
Commands that handle xunit results.
"""

import os
import logging
import xunitparser
import testbed.core.serializers
import argparse
from testbed.libexec import result

def xunit_result_get(testcase):
    """ Determine the results from the testcase. """

    if testcase.bad:
        raise NotSupported("bad testcase not supported")
    elif testcase.errored:
        raise NotSupported("erroed testcase not supported")
    elif testcase.failed:
        return "failed"
    elif testcase.good:
        return "pass"
    elif testcase.success:
        return "pass"
    elif testcase.skipped:
        return "skipped"
    else:
        raise ValueError("unknown testcase result")


def do_save(args):
    """ Save xunit results. """

    from testdb import models

    (testsuite, testresults) = xunitparser.parse(open(args.resultfile))

    for testcase in testsuite:
        testsuite_name = testcase.classname.split(".")[0]
        test_name = testcase.methodname
        test_result = xunit_result_get(testcase)

        logging.info("test %s.%s %s" % (testsuite_name, test_name, result))
        result.api.set_result(args.context, args.product, args.branch,
                              args.build, testsuite_name, test_name,
                              test_result, args.testkeys)


def add_subparser(subparser):
    """ Create testsuite CLI commands. """

    parser = subparser.add_parser(
        "xunit", help="commands related to results stored in xunit formater.",
        description=__doc__)
    parser.add_argument("--context", default="default", type=str,
                        help="Testsuite context.")
    subparser = parser.add_subparsers()
    parser = subparser.add_parser("save",
                                  help="Save xunit results into database.",
                                  description="store xunit result to database")

    parser.set_defaults(func=do_save)
    parser.add_argument("product", type=str, help="Name of product.")
    parser.add_argument("branch", type=str, help="Product branch name.")
    parser.add_argument("build", type=str, help="build.")
    parser.add_argument("resultfile", type=str, help="xunit result file.")
    parser.add_argument("testkeys", default=[], nargs=argparse.REMAINDER,
                        type=result.commands.valid_testkey,
                        help="Specify result for a test.")

    return subparser

