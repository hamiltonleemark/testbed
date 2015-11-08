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
    from testdb.models import TestProduct

    (context, _) = Context.objects.get_or_create(name=CONTEXT)
    product = Key.objects.get(value=product_name)

    find = TestProduct.objects.filter(context=context, product=product)
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
    from testdb.models import TestProduct
    from testdb.models import KVP

    logging.info("adding product %s %s", productname, branchname)

    ##
    # Make sure to track branch and product against KVP. This is done
    # incase user decides to make these keys strict.
    KVP.get_or_create("branch", branchname)
    KVP.get_or_create("product", productname)

    if order == -1:
        find = TestProduct.objects.filter(context__name=CONTEXT)
        try:
            order = find.order_by("-order")[0].order
        except IndexError:
            order = 0

        order += 1
        logging.info("using order %d", order)

    ##
    # Order is specified so now we have to move something.
    products = TestProduct.objects.filter(context__name=CONTEXT,
                                          order__gte=order).order_by("order")
    current_order = order
    for product in products:
        if product.order == current_order:
            product.order += 1
            logging.debug("updating order %s to %d", productname,
                          product.order)
            product.save()
            current_order = product.order

    (product, created) = TestProduct.get_or_create(CONTEXT, productname,
                                                   branchname)
    product.order = order
    product.save()

    return (product, created)


# pylint: disable=W0622
def contains(value=None):
    """ Retrieve the list of products based on product and or branch_name. """

    from testdb.models import TestProduct
    from testdb.models import Context

    (context, _) = Context.objects.get_or_create(name=CONTEXT)
    find = TestProduct.objects.filter(context=context)
    if value:
        find = find.filter(
            models.Q(product__value__contains=value) |
            models.Q(branch__value__contains=value) |
            models.Q(keys__key__value__contains=value))
    return find.order_by("order")


def remove(product, branch):
    """ Get or create a testplan in a certain order.
    Order is just that the location of the testplan in the list of testplans.
    The order effects the location the testplan appears on web pages.
    """

    from testdb.models import Testplan
    from testdb.models import Context
    from testdb.models import KVP

    print "MARK: remove product", product, branch

    try:
        branch_key = KVP.objects.get(key__value="branch", value=branch)
    except KVP.DoesNotExist, arg:
        raise Testplan.DoesNotExist(arg)

    try:
        context = Context.objects.get(name=CONTEXT)
    except Context.DoesNotExist, arg:
        raise Testplan.DoesNotExist(arg)

    find = Testplan.objects.filter(testsuite__context=context,
                                   testsuite__name__name=product,
                                   testsuite__keys=branch_key)
    for item in find:
        item.delete()
