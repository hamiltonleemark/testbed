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
Products consist of a name, a branch name and their test plans.

Products can have multiple
branches. The combination of product name and branch names are ordered
which effects how products are displayed. This order can be leveraged
in various ways such as defining the priority of branches that need testing.
"""
import logging
import yaml
from . import api
from testbed.libexec import testplan


def product_add(args):
    """ Add a product to the database. """
    return api.get_or_create(args.name, args.branch, args.order)


def product_remove(args):
    """ Add a product to the database. """
    return api.remove(args.product, args.branch)


def do_product_testplan_add(args):
    """ Add a testplan to the database. """
    from testdb import models

    logging.info("adding testplan %s to product %s %s", args.testplan,
                 args.product, args.branch)
    (product, _) = api.get_or_create(args.product, args.branch)
    product.key_get_or_create("testplan", args.testplan)

    context = models.Testplan.context_get(args.testplan)
    (testplan, created) = models.Testplan.objects.get_or_create(context=context)


def product_list(args):
    """ List products based on search criteria.

    list products in a dense manner.
    """

    from testdb import models
    logging.info("listing products")

    products = models.TestProduct.filter(api.CONTEXT,
                                         args.filter).order_by("order")
    root = {}
    for product in products:
        level = {
            product.order: "%s %s" % (str(product.product),
                                      str(product.branch))
            }

        testkeys = {str(item.testkey.key): str(item.testkey.value)
                    for item in product.testproductkeyset_set.all()}
        if testkeys:
            level["keys"] = testkeys

        context = str(product.context)
        if context not in root:
            root[context] = []
        root[context].append(level)
    print yaml.dump(root, default_flow_style=False)


def add_subparser(subparser):
    """ Create testsuite CLI commands. """

    parser = subparser.add_parser("product",
                                  help="setup and modify products",
                                  description=__doc__)
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
                        "next value.")
    ##
    # Add
    parser = subparser.add_parser(
        "remove",
        description="Remove a product to the database",
        help="Remove a product.")
    parser.set_defaults(func=product_remove)
    parser.add_argument("product", type=str, help="Name of the product.")
    parser.add_argument("branch", type=str, help="Branch name of the product.")

    ##
    # List
    parser = subparser.add_parser("list",
                                  description="List all of the products.",
                                  help="List products.")
    parser.set_defaults(func=product_list)
    parser.add_argument("--filter", type=str, help="Filter products")

    ##
    # Add testplan
    parser = subparser.add_parser(
        "testplan",
        description="Modify testplan for the product",
        help="Associate testplan to a product.")
    subparser = parser.add_subparsers()
    parser = subparser.add_parser(
        "add", description="Associate testplan to a product",
        help="add testplan to product.")

    parser.set_defaults(func=do_product_testplan_add)
    parser.add_argument("product", type=str, help="Product name.")
    parser.add_argument("branch", type=str, help="Branch name.")
    parser.add_argument("testplan", type=str, help="Name of testplan.")

    return subparser
