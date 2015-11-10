"""
Functionality common to more than one command.
"""
import logging

ROOT = "testplan"
CONTEXT = "default"
ORDER_NEXT = -1


# pylint: disable=R0914
def get_or_create(context, testsuite_name, order=ORDER_NEXT):
    """ Get or create a testplan and set order.

    Order is just that the location of the testplan in the list of
    testplans. The order effects the location the testplan appears on web
    pages.  When complete testplan order number is sequential with no gaps.
    @param testsuite_name The testsuite name for the testplan
    @param context Testplan context organizes testplans in a logical group.
                   Testplans with the same context are in the same group.
                   The order indicates the order of the testplan in the
                   context.
    @param order the location of testsuite in the testplan. To change the
                 order of an existing testplan pass in a different number.
    """

    from testdb.models import Testplan
    from testdb.models import TestplanOrder
    from testdb.models import TestsuiteName

    context = Testplan.context_get(context)
    (testplan, created) = Testplan.objects.get_or_create(context=context)

    if order == ORDER_NEXT:
        find = testplan.testplanorder_set.all()
        try:
            order = find.order_by("-order")[0].order + 1
        except IndexError:
            order = 1
        logging.info("using order %d", order)

    ##
    # Assert order is not -1.
    # Order is specified so now we have to move something.
    planorders = testplan.testplanorder_set.filter(order__gte=order)
    for item in planorders.order_by("order"):
        item.order += 1
        item.save()

    (name, _) = TestsuiteName.objects.get_or_create(name=testsuite_name)
    (_, created) = TestplanOrder.get_or_create(testplan, name, order)

    ##
    # Make sure test plan order entries are sequential with no gaps.
    order = 1
    for planorder in testplan.testplanorder_set.all().order_by("order"):
        if int(order) != int(planorder.order):
            planorder.order = order
            planorder.save()
        order += 1
    ##

    return (testplan, created)


def remove(context, order):
    """ Get or create a testplan in a certain order.

    @param context Testplan context organizes testplans in a logical group.
                   Testplans with the same context are in the same group.
                   The order indicates the order of the testplan in the
                   context.

    @param testsuite_name The testsuite name for the testplan
    """

    from testdb import models

    context = models.Testplan.context_get(context)
    testplan = models.Testplan.objects.get(context=context)
    order = testplan.testplanorder_set.get(order=order)
    if order:
        order.delete()
    ##
    # Make sure test plan order entries are sequential with no gaps.
    order = 1
    for planorder in testplan.testplanorder_set.all():
        if int(order) != int(planorder.order):
            planorder.order = order
            planorder.save()
        order += 1
    ##
    return True


def get(context, testkeys):
    """ Get testplan. """

    from testdb.models import Testplan

    context = Testplan.context_get(context)
    if len(testkeys) == 0:
        return Testplan.objects.get(context=context)
    else:
        find = Testplan.objects.filter(context=context)
        for testkey in testkeys[:-1]:
            find = find.filter(keys=testkey)
        return find.get(keys=testkeys[-1])


def add(context, testsuite_name, order):
    """ Add testsuite.

    Order is just that the location of the testplan in the list of testplans.
    The order effects the location the testplan appears on web pages.
    @param testsuite_name The testsuite name for the testplan
    @param context Testplan context organizes testplans in a logical group.
                   Testplans with the same context are in the same group.
                   The order indicates the order of the testplan in the
                   context.
    @param order the location of testsuite in the testplan. To change the order
                 of an existing testplan pass in a different number.
    """

    from testdb.models import Testplan
    from testdb.models import TestplanOrder
    from testdb.models import TestsuiteName

    context = Testplan.context_get(context)
    (testplan, created) = Testplan.objects.get_or_create(context=context)

    if order == ORDER_NEXT:
        find = testplan.testplanorder_set.all()
        try:
            order = find.order_by("-order")[0].order + 1
        except IndexError:
            order = 1
        logging.info("using order %d", order)

    ##
    # Assert order is not -1.
    # Order is specified so now we have to move something.
    planorders = testplan.testplanorder_set.filter(order__gte=order)
    current_order = order
    for prevplan in planorders.order_by("order"):
        if prevplan.order == current_order:
            prevplan.order += 1
            prevplan.save()
            current_order = prevplan.order

    (name, _) = TestsuiteName.objects.get_or_create(name=testsuite_name)
    (_, created) = TestplanOrder.create(testplan, name, order)
    return (testplan, created)


def add_key(context, order, key, value):
    """ Add a key into the testplan. """

    from testdb.models import Testplan
    logging.info("add %s=%s to testsuite %s %s", key, value, context, order)
    from testdb.models import Testsuite
    from testdb.models import KVP

    context = Testplan.context_get(context)
    testplan = Testplan.objects.get(context=context)
    planorder = testplan.testplanorder_set.get(order=order)
    testsuite = Testsuite.objects.get(context=context, testplanorder=planorder)
    (testkey, _) = KVP.get_or_create(key=key, value=value)
    testsuite.testsuitekeyset_set.get_or_create(testsuite=testsuite,
                                                testkey=testkey)

    return (testsuite, testkey)
