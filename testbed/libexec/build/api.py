"""
Functionality common to more than one command.
"""
import logging
import datetime


CONTEXT = "build.default"


# pylint: disable=R0914
def get_or_create(productname, branchname, buildname, when=None):
    """ Get or create a testplan in a certain order.
    @param product_name Is the name of the product
    @param order order is the location of the testplan in the list of
                 testplans. The order effects the location the testplan
                 appears on web pages.
    """
    from testdb import models

    if not when:
        when = datetime.datetime.now()

    logging.info("adding build %s %s %s %s", productname, branchname,
                 buildname, when)
    (context, _) = models.Context.objects.get_or_create(name=CONTEXT)
    (product, _) = models.TestKey.get_or_create("product", productname)
    (branch, _) = models.TestKey.get_or_create("branch", branchname)
    (build, _) = models.TestKey.get_or_create("build", buildname)

    testkeys = [product, branch, build]
    name = "%s.%s" % (productname, branchname)

    results = models.Testsuite.get_or_create(context, name, None, testkeys)

    return results


def build_list(productname, branchname=None):
    """ Return the list builds given the parameters. """
    from testdb import models

    logging.info("list build %s %s", productname, branchname)
    (context, _) = models.Context.objects.get_or_create(name=CONTEXT)
    find = models.Testsuite.objects.filter(context=context)

    if productname:
        (product, _) = models.TestKey.get_or_create("product", productname)
        find = find.filter(keys=product)

    if branchname:
        (branch, _) = models.TestKey.get_or_create("branch", branchname)
        find = find.filter(keys=branch)

    return [item.key_get("build") for item in find]
