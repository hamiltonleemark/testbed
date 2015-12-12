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
Functionality common to more than one command.
"""
import logging
from testbed.libexec import product
from testbed.libexec import planorder
from testbed.libexec import testplan


# pylint: disable=R0913
# pylint: disable=R0914
def set_result(context, product_name, branch_name, build, testsuite_name,
               test_name, result, testkeys):
    """ Get or create a testplan in a certain order.

    @param product_name Is the name of the product
    @param order order is the location of the testplan in the list of
                 testplans. The order effects the location the testplan
                 appears on web pages.
    @param testkeys list of tuples of the form (key,value)
    """
    from testdb import models

    logging.debug("%s %s %s %s", product_name, branch_name, build,
                  testsuite_name)

    product1 = models.Product.get(product.api.CONTEXT,
                                  product_name, branch_name)

    testplan_name = product1.key_get("testplan", None)
    if testplan_name is None:
        raise ValueError("product %s %s missing testplan" % (product_name,
                                                             branch_name))
    ##
    # Make sure testsuite and test are part of the test plan.
    order = planorder.api.get(testplan_name, testsuite_name, testkeys)
    ##

    build_key = models.KVP.get_or_create("build", build)[0]
    (context, created) = models.Context.objects.get_or_create(name=context)
    (testsuite1, critem) = models.Testsuite.get_or_create(
        context, testsuite_name, order, build_key, [])
    created = created or critem

    (test, critem) = models.Test.get_or_create(testsuite1, test_name, result,
                                               [])
    created = created or critem
    return (test, created)


# pylint: disable=W0622
def list_result(context, product_name, branch_name, testkeys, build=None):
    """ Retrieve the list of products based on product and or branch_name. """
    from testdb import models

    products1 = product.api.filter(product_name, branch_name)
    context = models.Context.objects.get(name=context)
    for product1 in products1:
        testplan_name = product1.key_get("testplan")
        testsuites = testplan.api.list_testsuite(testplan_name, testkeys,
                                                 build)
        for testsuite_item in testsuites:
            for test in testsuite_item.test_set.all():
                yield (testsuite_item, test)
