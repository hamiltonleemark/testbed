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

    print "MARK: add testsuite 1", models.Testplan.objects.all()
    testplanorder = testplan.api.planorder_get(testplan.api.CONTEXT,
                                               testsuite_name, testkeys)
    print "MARK: add testsuite 2", models.Testplan.objects.all()
    testkeys = [models.TestKey.get_or_create(key, value)[0]
                for (key, value) in testkeys]
    print "MARK: add testsuite 3"

    return models.Testsuite.get_or_create(context, testsuite_name, testkeys)


def list_testsuite(context, testkeys, testsuite_name=None):
    """ Retrieve the list of products based on product and or branch_name. """

    from testdb import models

    if context:
        find = models.Testsuite.objects.filter(context__name=context)
    else:
        find = models.Testsuite.objects.filter

    if testsuite_name:
        find = find.filter(name__name=testsuite_name)

    for testkey in testkeys:
        find = find.filter(keys=testkey)

    return find
