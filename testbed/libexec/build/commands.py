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
Products consist of a name, a branch name and their test plans.

Products can have multiple
branches. The combination of product name and branch names are ordered
which effects how products are displayed. This order can be leveraged
in various ways such as defining the priority of branches that need testing.
"""
import logging
import yaml
from . import api


def do_build_add(args):
    """ Add a product to the database. """
    return api.get_or_create(args.product, args.branch, args.build)


def do_build_list(args):
    """ List builds for a product.  """

    from testdb import models
    from testdb import builds

    logging.info("listing builds")

    (context, _) = models.Context.objects.get_or_create(name=builds.CONTEXT)

    find = models.Testsuite.objects.filter(context=context)
    if args.product:
        (product, _) = models.TestKey.get_or_create("product", args.product)
        find = find.filter(testkey=product)

    if args.branch:
        (branch, _) = models.TestKey.get_or_create("branch", args.branch)
        find = find.filter(testkey=branch)

    find = find.order_by("timestamp")

    root = {}
    for build in find:
        name = str(build.name)

        if name not in root:
            root[name] = []

        root[name].append(str(build.key_get("build")))

    print yaml.dump(root, default_flow_style=False)


def add_subparser(subparser):
    """ Create testsuite CLI commands. """

    parser = subparser.add_parser("build",
                                  help="Add product build information",
                                  description=__doc__)
    subparser = parser.add_subparsers()

    ##
    # Add
    parser = subparser.add_parser("add",
                                  description="Add a build for a product",
                                  help="Add a product build.")
    parser.set_defaults(func=do_build_add)
    parser.add_argument("product", type=str, help="Name of the product.")
    parser.add_argument("branch", type=str, help="Name of the product branch.")
    parser.add_argument("build", type=str, help="Build identifier.")

    # List
    parser = subparser.add_parser("list",
                                  description="List all product builds.",
                                  help="list all product builds.")
    parser.set_defaults(func=do_build_list)
    parser.add_argument("--product", type=str, help="Name of the product.")
    parser.add_argument("--branch", type=str,
                        help="Name of the product branch.")

    return subparser
