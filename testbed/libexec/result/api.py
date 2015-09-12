"""
Functionality common to more than one command.
"""
import logging


# pylint: disable=R0913
# pylint: disable=R0914
def set_result(context, product, branch, build, testsuite, test, result,
               testkeys=None):
    """ Get or create a testplan in a certain order.

    @param product_name Is the name of the product
    @param order order is the location of the testplan in the list of
                 testplans. The order effects the location the testplan
                 appears on web pages.
    """
    from testdb import models

    if not testkeys:
        testkeys = []
    testkeys = [models.TestKey.get_or_create(key, value)[0]
                for (key, value) in testkeys]

    logging.info("result for %s %s %s %s %s %s", product, branch, build,
                 testsuite, test, result)

    (product, _) = models.TestKey.get_or_create("product", product)
    (branch, _) = models.TestKey.get_or_create("branch", branch)
    (build, _) = models.TestKey.get_or_create("build", build)
    (testname, _) = models.TestName.objects.get_or_create(name=test)
    (testsuite, _) = models.Testsuite.get_or_create(context, testsuite,
                                                    testkeys)
    testkeys += [product, branch, build]
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

    if context:
        find = models.Test.objects.filter(testsuite__context__name=context)
    else:
        find = models.Test.objects.filter

    if testsuite_name:
        find = find.filter(testsuite__name__name=testsuite_name)
    if test_name:
        find = find.filter(test__name=test_name)

    for (key, value) in testkeys:
        (testkey, _) = models.TestKey.get_or_create(key, value)
        find = find.filter(testsuite__keys=testkey)

    return find
