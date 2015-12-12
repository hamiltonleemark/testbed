# (c) 2015 Mark Hamilton, <mark.lee.hamilton@gmail.com>
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

import logging
import subprocess
import re
from testbed.libexec import testplan


def do_testplan(args):
    """ Save xunit results. """

    ##
    # path1/path2/testsuite.py::class::test_name
    regexp = re.compile(r"/([\w]+)\.py::[\w\.]+::([\w\.]+)")

    from testdb import models

    cmd = ["py.test", "-q", "--collect-only", args.dir]
    lines = subprocess.check_output(cmd)
    for line in lines.split("\n"):
        if len(line) == 0:
            break

        groups = regexp.search(line)
        testsuite_name = groups.group(1)
        test_name = groups.group(2)
        (_, testsuite, _) = testplan.api.get_or_create(args.testplan_name,
                                                       testsuite_name)
        models.Test.get_or_create(testsuite, test_name, "pass", [])
        logging.info("adding %s %s to testplan %s", testsuite_name, test_name,
                     args.testplan_name)


def add_subparser(subparser):
    """ Create testsuite CLI commands. """

    parser = subparser.add_parser(
        "pytest", help="commands related to py.test framework.",
        description=__doc__)
    subparser = parser.add_subparsers()
    parser = subparser.add_parser("testplan",
                                  help="Save xunit results into database.",
                                  description="store xunit result to database")

    parser.set_defaults(func=do_testplan)
    parser.add_argument("testplan_name", type=str, help="Testplan name.")
    parser.add_argument("dir", type=str, help="Product branch name.")

    return subparser
