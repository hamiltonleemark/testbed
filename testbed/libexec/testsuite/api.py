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
from testbed.libexec import testplan
from testbed.libexec import planorder


def add_testsuite(context, testsuite_name, build, testkeys):
    """ Add a testsuite to the database. """

    from testdb import models
    logging.info("adding testsuite %s", testsuite_name)

    if testkeys is None:
        testkeys = []

    ##
    # \todo Keep only testkeys that are associated to a testplan
    testplanorder = planorder.api.get(testplan.api.CONTEXT, testsuite_name,
                                      testkeys)
    buildkey = models.KVP.get_or_create("build", build)[0]
    return models.Testsuite.get_or_create(context, testsuite_name,
                                          testplanorder, buildkey, [])


# \todo This should be called filter
def list_testsuite(context, testkeys, build=None, testsuite_name=None):
    """ Retrieve the list of testsuites by tesykeys and name. """

    from testdb import models

    ##
    # First find the testplan and the order in which test tests should be
    # presented.

    ##
    # \todo Keep only testkeys that are associated to a testplan
    testkeys = [models.KVP.get_or_create(key, value)[0]
                for (key, value) in testkeys]
    testplan1 = testplan.api.get(context, testkeys)
    if build:
        testkeys += [models.KVP.get_or_create("build", build)[0]]

    if testsuite_name:
        orders = testplan1.testplanorder_set.filter(name__name=testsuite_name)
    else:
        orders = testplan1.testplanorder_set.all()

    orders = orders.order_by("order")

    ##
    # Given the order now find the list of testsuites.
    (context, _) = models.Context.objects.get_or_create(name=context)
    for order in orders:
        testsuites = models.Testsuite.filter(context=context, order=order,
                                             keys=testkeys)
        for item in testsuites:
            yield item
