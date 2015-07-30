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
CLI for testsuites.
"""
import logging
import sys

LOGGER = logging.getLogger(__name__)


def add_testsuite(args):
    """ Add a testsuite to the database. """

    import tests.models as models

    LOGGER.info("adding testsuite %s", args.name)
    name = models.TestsuiteName.objects.get_or_create(name=args.name)
    models.Testsuite.get_or_create("default", name, [])


def list_testsuite(args):
    """ List testsuites based on search criteria. """
    from dbsite.tests import models

    LOGGER.info("listing testsuites %s", args.name)
    for item in Testsuite.object.all():
        print item



def add_subparser(subparser):
    """ Create testsuite CLI commands. """

    parser = subparser.add_parser("testsuite", help=__doc__)
    subparser = parser.add_subparsers()

    ##
    # Add
    parser = subparser.add_parser("add",
                                  description="Add a testsuite",
                                  help="Add a testsuite.")
    parser.set_defaults(func=add_testsuite)
    parser.add_argument("name", type=str, help="Name of the testsuite.")

    ##
    # Remove
    parser = subparser.add_parser("remove",
                                  description="Remove a testsuite.",
                                  help="Remove a testsuite.")
    parser.add_argument("name", type=str, help="name of the testsuite.")

    return subparser
