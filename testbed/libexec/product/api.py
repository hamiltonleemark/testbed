"""
Functionality common to more than one command.
"""
import logging
from django.db import models

CONTEXT = "product.default"


def get_or_create(product_name, branch_name, order=-1):
    """ Get or create a testplan in a certain order.
    @param order order is the location of the testplan in the list of
                 testplans. The order effects the location the testplan
                 appears on web pages.
    """

    from testdb.models import Testplan
    from testdb.models import Testsuite
    from testdb.models import Context
    from testdb.models import TestKey

    (branch_key, _) = TestKey.get_or_create("branch", branch_name)
    (context, _) = Context.objects.get_or_create(name=CONTEXT)
    if order == -1:
        find = Testplan.objects.filter(testsuite__context=context,
                                       testsuite__keys=branch_key)
        try:
            order = find.order_by("-order")[0].order + 1
        except IndexError:
            order = 1
        logging.info("using order %d", order)

    ##
    # Order is specified so now we have to move something.
    testplans = Testplan.objects.filter(testsuite__context=context,
                                        order__gte=order).order_by("order")
    current_order = order
    for testplan in testplans:
        if testplan.order == current_order:
            testplan.order += 1
            testplan.save()
            current_order += 1

    (testsuite, _) = Testsuite.get_or_create(CONTEXT, product_name,
                                             [branch_key])
    return Testplan.get_or_create(testsuite=testsuite, order=order)


# pylint: disable=W0622
def filter(value=None):
    """ Retrieve the list of products based on product and or branch_name. """

    from testdb.models import Testplan
    from testdb.models import Context

    (context, _) = Context.objects.get_or_create(name=CONTEXT)
    find = Testplan.objects.filter(testsuite__context=context)
    if value:
        find = find.filter(
            models.Q(testsuite__name__name__contains=value) |
            models.Q(testsuite__keys__key__value__contains=value))
    return find.order_by("order")


def remove(product_name, branch_name):
    """ Get or create a testplan in a certain order.
    Order is just that the location of the testplan in the list of testplans.
    The order effects the location the testplan appears on web pages.
    """

    from testdb.models import Testplan
    from testdb.models import Context
    from testdb.models import TestKey

    try:
        branch_key = TestKey.objects.get(key__value="branch",
                                         value=branch_name)
    except TestKey.DoesNotExist, arg:
        raise Testplan.DoesNotExist(arg)

    try:
        context = Context.objects.get(name=CONTEXT)
    except Context.DoesNotExist, arg:
        raise Testplan.DoesNotExist(arg)

    find = Testplan.objects.filter(testsuite__context=context,
                                   testsuite__name__name=product_name,
                                   testsuite__keys=branch_key)
    for item in find:
        item.delete()
