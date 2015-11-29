"""
Functionality common to more than one command.
"""
import logging
import datetime


# pylint: disable=R0914
def get_or_create(productname, branchname, buildname, when=None):
    """ Get or create a testplan in a certain order.
    @param product_name Is the name of the product
    @param order order is the location of the testplan in the list of
                 testplans. The order effects the location the testplan
                 appears on web pages.
    """
    from testdb import models
    from testdb import builds

    if not when:
        when = datetime.datetime.now()

    logging.info("adding build %s %s %s %s", productname, branchname,
                 buildname, when)
    (context, _) = models.Context.objects.get_or_create(name=builds.CONTEXT)
    (product, _) = models.KVP.get_or_create("product", productname)
    (branch, _) = models.KVP.get_or_create("branch", branchname)
    (build_key, _) = models.KVP.get_or_create("build", buildname)

    testkeys = [product, branch]
    name = "%s.%s" % (productname, branchname)

    # \todo testsuite should point to product
    results = models.Testsuite.get_or_create(context, name, None, build_key,
                                             testkeys)

    return results


# pylint: disable=W0622
def filter(product_name, branch_name=None):
    """ Return the list builds given the parameters. """
    from testdb import builds
    from testdb import models

    (product_name, _) = models.KVP.get_or_create("product", product_name)
    if branch_name:
        (branch_name, _) = models.KVP.get_or_create("branch", branch_name)

    builds = builds.filter(product_name, branch_name)

    builds = [item.key_get("build") for item in builds]
    return [item.value for item in builds]
# pylint: enable=W0622
