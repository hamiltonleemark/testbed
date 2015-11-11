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
               test_name, result, keys):
    """ Get or create a testplan in a certain order.

    @param product_name Is the name of the product
    @param order order is the location of the testplan in the list of
                 testplans. The order effects the location the testplan
                 appears on web pages.
    """
    from testdb import models

    logging.debug("result for %s %s %s", testsuite_name, test_name, result)

    (product1, created) = product.api.get_or_create(product_name, branch_name)

    testplan_name = product1.key_get("testplan", None)
    if testplan_name is None:
        raise ValueError("product %s %s missing testplan" % (product_name,
                                                             branch_name))
    ##
    # Make sure testsuite is part of the test plan.
    (order, critem) = planorder.api.get_or_create(testplan_name,
                                                  testsuite_name, test_name,
                                                  keys)
    created = created or critem
    ##

    build_key = models.KVP.get_or_create("build", build)[0]
    (context, _) = models.Context.objects.get_or_create(name=context)
    (testsuite2, critem) = models.Testsuite.get_or_create(context,
                                                          testsuite_name,
                                                          order, build_key, [])
    created = created or critem

    (test, critem) = models.Test.get_or_create(testsuite2, test_name, [])
    created = created or critem

    if result == "pass":
        test.status = 0
    else:
        test.status = 1
    test.save()
    return (test, created)


# pylint: disable=W0622
def list_result(context, testkeys, build=None):
    """ Retrieve the list of products based on product and or branch_name. """

    testsuites = testplan.api.list_testsuite(context, testkeys, build)
    for testsuite_item in testsuites:
        for test in testsuite_item.test_set.all():
            yield (testsuite_item, test)
