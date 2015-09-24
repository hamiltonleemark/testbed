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


def add_testsuite(context, testsuite_name, testkeys):
    """ Add a testsuite to the database. """

    from testdb import models
    logging.info("adding testsuite %s", testsuite_name)

    ##
    # \todo Keep only testkeys that are associated to a testplan
    testplankeys = [item for item in testkeys if item[0] != "build"]

    testplanorder = testplan.api.planorder_get(testplan.api.CONTEXT,
                                               testsuite_name, testplankeys)
    testkeys = [models.TestKey.get_or_create(key, value)[0]
                for (key, value) in testkeys if key == "build"]
    return models.Testsuite.get_or_create(context, testsuite_name,
                                          testplanorder, testkeys)

# \todo This should be called filter
def list_testsuite(context, testkeys, testsuite_name=None):
    """ Retrieve the list of testsuite testkeys. """

    from testdb import models

    ##
    # First find the testplan and the order in which test tests  should be
    # presented.

    ##
    # \todo Keep only testkeys that are associated to a testplan
    testplankeys = [item for item in testkeys if item.key.value != "build"]
    testplan1 = testplan.api.get(testplan.api.CONTEXT, testplankeys)
    testkeys = [item for item in testkeys if item.key.value == "build"]

    if testsuite_name:
        orders = testplan1.testplanorder_set.filter(name__name=testsuite_name)
    else:
        orders = testplan1.testplanorder_set.all()

    ##
    # Given the order now find the list of testsuites.
    (context, _) = models.Context.objects.get_or_create(name=context)
    for order in orders:
        print "MARK: list_testsuite 1", order
        for testsuite in models.Testsuite.filter(context, order, testkeys):
            print "MARK: list_testsuite 2", order, testsuite
            yield testsuite
