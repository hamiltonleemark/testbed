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

    Order is just that the location of the testplan in the list of testplans.
   The order effects the location the testplan appears on web pages.
    When complete testplan order number is sequential with no gaps.
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


def planorder_get(context, testsuite_name, keys):
    """ Return TestplanOrder. """

    from testdb import models

    testkeys = [models.KVP.get_or_create(key=key, value=value)[0]
                for (key, value) in keys]

    context = models.Testplan.context_get(context)
    find = models.Testplan.objects.filter(context=context)
    for testkey in testkeys:
        find = find.filter(keys=testkey)

    testplans = [item for item in find]
    if len(testplans) == 0:
        return None
    name = models.TestsuiteName.objects.get(name=testsuite_name)

    # \todo deal with many test plan or zero.
    return models.TestplanOrder.objects.get(testplan=testplans[0],
                                            testsuite__context=context,
                                            testsuite__name=name)


def planorder_get_or_create(context, testsuite_name, test_name, keys):
    """ Return TestplanOrder. """

    from testdb import models

    testkeys = [models.KVP.get_or_create(key=key, value=value)[0]
                for (key, value) in keys]

    context = models.Testplan.context_get(context)
    find = models.Testplan.objects.filter(context=context)
    for testkey in testkeys:
        find = find.filter(keys=testkey)

    testplans = [item for item in find]
    if len(testplans) == 0:
        return (None, False)

    (name, _) = models.TestsuiteName.objects.get_or_create(name=testsuite_name)

    # \todo deal with many test plan or zero.
    (order, critem) = models.TestplanOrder.objects.get_or_create(
        testplan=testplans[0], testsuite__context=context,
        testsuite__name=name)

    for testsuite1 in order.testsuite_set.filter(context=context):
        # /todo this should return (object, created)
        (_, critem) = models.Test.get_or_create(testsuite1, test_name, [])
        return (order, critem)
    return (None, False)


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
