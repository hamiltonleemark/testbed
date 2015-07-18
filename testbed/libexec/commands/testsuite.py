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
import argparse


def add_testsuite(args):
    """ Add a testsuite to the database. """
    print "MARK: args", args


def add_subparser(subparser):
    """ Create testsuite CLI commands. """

    parser = subparser.add_parser("testsuite")

    subparser = parser.add_subparsers()
    parser = subparser.add_parser("add",
                                  description="Add a testsuite",
                                  help="Add a testsuite.")
    parser.add_argument("name", type=str,
                        help="add a testsuite")
    parser.set_defaults(func=add_testsuite)
    parser = subparser.add_parser("remove")
    parser.add_argument("name", type=str,
                        help="add a testsuite")

    return subparser
