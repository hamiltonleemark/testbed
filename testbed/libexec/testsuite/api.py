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
CLI for testsuites.
"""
import logging
from testbed.libexec import planorder


# \todo change order testplan_name after context
def add_testsuite(testplan_name, context, testsuite_name, build, testkeys):
    """ Add a testsuite to the database. """

    from testdb import models
    logging.info("adding testsuite %s", testsuite_name)

    if testkeys is None:
        testkeys = []

    ##
    # \todo Keep only testkeys that are associated to a testplan
    testplanorder = planorder.api.get(testplan_name, testsuite_name, testkeys)
    buildkey = models.KVP.get_or_create("build", build)[0]
    return models.Testsuite.get_or_create(context, testsuite_name,
                                          testplanorder, buildkey, [])
