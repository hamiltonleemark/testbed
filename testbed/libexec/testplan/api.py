"""
Functionality common to more than one command.
"""
import logging

ROOT = "testplan"
CONTEXT = "default"
ORDER_NEXT = -1
ORDER_FIRST = 0


# pylint: disable=R0914
def get_or_create(testplan_name, testsuite_name, order=ORDER_NEXT):
    """ Get or create a testplan and set order.

    Order is just that the location of the testplan in the list of
    testplans. The order effects the location the testplan appears on web
    pages.  When complete testplan order number is sequential with no gaps.
    @param testsuite_name The testsuite name for the testplan
    @param testplan_name Testplan context organizes testplans in a logical
                         group. Testplans with the same context are in the
                         same group. The order indicates the order of the
                         testplan.
    @param order the location of testsuite in the testplan. To change the
                 order of an existing testplan pass in a different number.
    """
    from testdb.models import Testplan
    from testdb.models import TestplanOrder
    from testdb.models import TestsuiteName

    testplan_name = Testplan.context_get(testplan_name)
    (testplan, _) = Testplan.objects.get_or_create(context=testplan_name)
    (name, _) = TestsuiteName.objects.get_or_create(name=testsuite_name)

    try:
        (_, testsuite) = TestplanOrder.get(testplan, name)
        return (testplan, testsuite, False)
    except TestplanOrder.DoesNotExist:
        if order == ORDER_NEXT:
            find = testplan.testplanorder_set.all()
            try:
                ##
                # find the last item.
                order = find.order_by("-order")[0].order + 1
            except IndexError:
                order = ORDER_FIRST
            logging.info("using order %d", order)

        ##
        # Assert order is not -1.
        # Order is specified so now we have to move something.
        planorders = testplan.testplanorder_set.filter(order__gte=order)
        new_order = order
        for item in planorders.order_by("order"):
            if new_order == item.order:
                item.order += 1
                item.save()
                new_order += 1

        (_, testsuite) = TestplanOrder.create(testplan, name, order)
        return (testplan, testsuite, True)


def pack(testplan_name):
    """ Pack testplan sequentially with no gaps."""
    from testdb.models import Testplan

    testplan_name = Testplan.context_get(testplan_name)
    testplan = Testplan.objects.get(context=testplan_name)

    ##
    # Make sure test plan order entries are sequential with no gaps.
    order = ORDER_FIRST
    for planorder in testplan.testplanorder_set.all().order_by("order"):
        if int(order) != int(planorder.order):
            planorder.order = order
            planorder.save()
        order += 1
    ##

    return True


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


def remove_key(context, order, key):
    """ Remove a key from the testplan. """

    from testdb.models import Testplan
    from testdb.models import Testsuite

    logging.info("remove %s from testsuite %s %s", key, context, order)

    context = Testplan.context_get(context)
    testplan = Testplan.objects.get(context=context)
    planorder = testplan.testplanorder_set.get(order=order)

    testsuite = Testsuite.objects.get(context=context, testplanorder=planorder)
    chitem = testsuite.key_remove(key)
    return chitem


def add_key(context, order, key, value):
    """ Add a key into the testplan. """

    from testdb.models import Testplan
    from testdb.models import Testsuite
    from testdb.models import Key
    from testdb.models import KVP

    logging.info("add %s=%s to testsuite %s %s", key, value, context, order)

    context = Testplan.context_get(context)
    testplan = Testplan.objects.get(context=context)
    planorder = testplan.testplanorder_set.get(order=order)
    testsuite = Testsuite.objects.get(context=context, testplanorder=planorder)
    (testkey, _) = KVP.get_or_create(key=key, value=value)
    testsuite.key_change(testkey)

    ##
    #

    (key, _) = Key.objects.get_or_create(value=key)
    testplan.testplankeyset_set.get_or_create(key=key)

    #
    ##
    return (testsuite, testkey)


# \todo This should be called filter
def list_testsuite(testplan_name, testkeys, build=None,
                   testsuite_context="default"):
    """ Retrieve the list of testsuites by tesykeys and name. """

    from testdb import models

    ##
    # First find the testplan and the order in which tests should be presented.

    testkeys = [models.KVP.get_or_create(key, value)[0]
                for (key, value) in testkeys]
    testplan1 = get(testplan_name, testkeys)
    orders = testplan1.testplanorder_set.filter().order_by("order")
    for testkey in testkeys:
        orders = orders.filter(testsuite__testkey=testkey)

    ##
    # Given the order now find the list of testsuites.
    (context, _) = models.Context.objects.get_or_create(name=testsuite_context)

    try:
        buildkeys = [models.KVP.get("build", build)]
    except models.KVP.DoesNotExist:
        buildkeys = []

    testsuites = models.Testsuite.filter(context, None, buildkeys)
    for order in orders:
        for item in testsuites.filter(testplanorder=order):
            yield item


def change(testplan_name, testsuite_name, order):
    """ Change the order of the testsuite.

    Order is just that the location of the testplan in the list of
    testplans. The order effects the location the testplan appears on web
    pages.  When complete testplan order number is sequential with no gaps.
    @param testsuite_name The testsuite name for the testplan
    @param testplan_name Testplan context organizes testplans in a logical
                         group. Testplans with the same context are in the
                         same group. The order indicates the order of the
                         testplan.
    @param order the location of testsuite in the testplan. To change the
                 order of an existing testplan pass in a different number.
    """
    from testdb.models import Testplan
    from testdb.models import TestplanOrder
    from testdb.models import TestsuiteName

    try:
        testplan_name = Testplan.context_get(testplan_name)
        testplan = Testplan.objects.get(context=testplan_name)
        name = TestsuiteName.objects.get(name=testsuite_name)
    except Testplan.DoesNotExist:
        raise TestplanOrder.DoesNotExist("TestplanOrder: %s %s does not exist".
                                         testplan_name, testsuite_name)
    (planorder, testsuite) = TestplanOrder.get(testplan, name)

    if order == ORDER_NEXT:
        find = testplan.testplanorder_set.all()
        try:
            ##
            # find the last item.
            order = find.order_by("-order")[0].order + 1
        except IndexError:
            order = ORDER_FIRST
        logging.info("using order %d", order)

    ##
    # Assert order is not -1.
    # Order is specified so now we have to move something.
    planorders = testplan.testplanorder_set.filter(order__gte=order)
    new_order = order
    for item in planorders.order_by("order"):
        if new_order == item.order:
            item.order += 1
            item.save()
            new_order += 1

    planorder.order = order
    planorder.save()
    return (testplan, testsuite)
