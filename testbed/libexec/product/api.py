"""
Functionality common to more than one command.
"""
import logging
from django.db import models

CONTEXT = "product.default"


# pylint: disable=R0914
# pylint: disable=W0622
# \todo this should be named branches
def filter(product_name, branch_name=None):
    """ Return list of products based on name and branch name. """

    from testdb.models import Context
    from testdb.models import Key
    from testdb.models import Product

    (context, _) = Context.objects.get_or_create(name=CONTEXT)
    product = Key.objects.get(value=product_name)

    find = Product.objects.filter(context=context, product=product)
    if branch_name:
        branch = Key.objects.get(value=branch_name)
        find = find.filter(branch=branch)
    return find
# pylint: enable=W0622


def get_or_create(productname, branchname, order=-1):
    """ Get or create a testplan in a certain order.

    @param product_name Is the name of the product
    @param order order is the location of the testplan in the list of
                 testplans. The order effects the location the testplan
                 appears on web pages.
    """
    from testdb.models import Product
    from testdb.models import KVP

    logging.info("adding product %s %s", productname, branchname)

    ##
    # Make sure to track branch and product against KVP. This is done
    # incase user decides to make these keys strict.
    KVP.get_or_create("branch", branchname)
    KVP.get_or_create("product", productname)

    if order == -1:
        find = Product.objects.filter(context__name=CONTEXT)
        try:
            order = find.order_by("-order")[0].order
        except IndexError:
            order = 0

        order += 1
        logging.info("using order %d", order)

    ##
    # Order is specified so now we have to move something.
    products = Product.objects.filter(context__name=CONTEXT,
                                      order__gte=order).order_by("order")
    current_order = order
    for product in products:
        if product.order == current_order:
            product.order += 1
            logging.info("updating order %s to %d", productname,
                         product.order)
            product.save()
            current_order = product.order

    (product, created) = Product.get_or_create(CONTEXT, productname,
                                               branchname)
    product.order = order
    product.save()

    return (product, created)


# pylint: disable=W0622
def contains(value=None):
    """ Retrieve the list of products based on product and or branch_name. """

    from testdb.models import Product
    from testdb.models import Context

    (context, _) = Context.objects.get_or_create(name=CONTEXT)
    find = Product.objects.filter(context=context)
    if value:
        find = find.filter(
            models.Q(product__value__contains=value) |
            models.Q(branch__value__contains=value) |
            models.Q(keys__key__value__contains=value))
    return find.order_by("order")


def remove(product, branch):
    """ Remove a product given name and branch. """

    from testdb.models import Product
    from testdb.models import Context
    from testdb.models import Key
    from testdb.models import KVP
    from testdb.models import Testplan
    from testdb.models import TestsuiteKVP
    from testdb import builds

    logging.info("removing %s %s", product, branch)
    try:
        context = Context.objects.get(name=CONTEXT)
        product1 = Product.objects.get(context=context, product__value=product,
                                       branch__value=branch)
    except (Context.DoesNotExist, Key.DoesNotExist), arg:
        logging.info("product  %s %s not found", product, branch)
        raise Product.DoesNotExist(arg)

    try:
        product_kvp = KVP.objects.get(key__value="product", value=product)
        branch_kvp = KVP.objects.get(key__value="branch", value=branch)
        buildids = builds.filter(product_kvp, branch_kvp)
    except KVP.DoesNotExist, arg:
        raise Product.DoesNotExist(arg)

    testplan_name = product1.key_get("testplan", None)
    testplan_context = Testplan.context_get(testplan_name)
    testplan = Testplan.objects.get(context=testplan_context)
    for testplan in testplan.testplanorder_set.all():
        for buildid in buildids:
            try:
                build = buildid.key_get("build")
                logging.info("removing %s %s %s", product, branch, build)
                for testsuite1 in testplan.testsuite_set.filter(kvps=build):
                    logging.info("removing %s %s %s %s", product, branch,
                                 buildid, testsuite1)
                    testsuite1.delete()
                buildid.delete()
            except TestsuiteKVP.DoesNotExist:
                continue
    testplan.delete()
    product1.delete()


def add_testplan(product, branch, testplan_name):
    """ Add testplan to product. """
    from testdb.models import Testplan

    (product1, _) = get_or_create(product, branch)

    context = Testplan.context_get(testplan_name)
    Testplan.objects.get_or_create(context=context)
    product1.key_get_or_create("testplan", testplan_name)
