"""
Functionality common to more than one command.
"""
import logging
from testbed.libexec import testplan
from testbed.libexec import testsuite


# pylint: disable=R0913
# pylint: disable=R0914
def set_result(context, product, branch, build, testsuite, test, result,
               keys=None):
    """ Get or create a testplan in a certain order.

    @param product_name Is the name of the product
    @param order order is the location of the testplan in the list of
                 testplans. The order effects the location the testplan
                 appears on web pages.
    """
    from testdb import models

    if not keys:
        keys = []

    testkeys = [models.TestKey.get_or_create(key, value)[0]
                for (key, value) in keys]

    logging.info("result for %s %s %s %s %s %s", product, branch, build,
                 testsuite, test, result)

    (product, _) = models.TestKey.get_or_create("product", product)
    (branch, _) = models.TestKey.get_or_create("branch", branch)
    (build, _) = models.TestKey.get_or_create("build", build)
    (testname, _) = models.TestName.objects.get_or_create(name=test)

    print "MARK: set_result", testplan.api.CONTEXT, keys
    planorder = testplan.api.planorder_get(testplan.api.CONTEXT, testsuite, keys)
    if planorder is None:
        raise ValueError("plan missing %s.%s" % (testplan.api.CONTEXT, testsuite))
    print "MARK: set_result planorder", planorder.id

    testkeys = [product, branch, build]
    (testsuite, _) = models.Testsuite.get_or_create(context, testsuite,
                                                    planorder, testkeys)
    print "MARK: set_result testsuite", context, testsuite
    (test, _) = models.Test.get_or_create(testsuite, testname, [])

    if result == "pass":
        test.status = 0
    else:
        test.status = 1
    test.save()

    return test


# pylint: disable=W0622
def list_result(context, testkeys, testsuite_name=None, test_name=None):
    """ Retrieve the list of products based on product and or branch_name. """

    from testdb import models

    print "MARK: context", context

    context = models.Context.objects.get(name=context)
    testsuites = testsuite.api.list_testsuite(context, testkeys,
                                              testsuite_name)

    for testsuite_item in testsuites:
        print "MARK: list_result", testsuite_item
        if test_name:
            find = find.filter(test__name=test_name)
        else:
            find = testsuite_item.test_set.all()

        print "MARK: list_result count", find.count()
        for test in find:
            print "  MARK: test", test
            yield (testsuite_item, test)
