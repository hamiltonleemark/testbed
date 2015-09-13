"""
Functionality common to more than one command.
"""
import logging

CONTEXT = "testplan.default"
ORDER_NEXT = -1


def get_or_create(context, testsuite_name, order):
    """ Get or create a testplan in a certain order.
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
    from testdb.models import Testsuite
    from testdb.models import Context

    (context, _) = Context.objects.get_or_create(name=context)
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

    (testsuite, _) = Testsuite.get_or_create(context, testsuite_name, None)
    (_, created) = TestplanOrder.get_or_create(testplan, testsuite, order)
    return (testplan, created)


def planorder_get(context, testsuite_name, keys):
    """ Return TestplanOrder. """
    from testdb import models

    context = models.Context.objects.get(name=context)
    testplan = models.Testplan.objects.get(context=context)
    testkeys = []
    for (key, value) in keys:
        print "MARK: testplan keys", key, value
        (testkey, _) = models.TestKey.get_and_check(key=key, value=value)
        testkeys.append(testkey)
        print "MARK: testplan keys after", key, value
    find = testplan.testplanorder_set.filter()
    for testkey in testkeys:
        find = find.filter(testkeys=testkey)
        print "MARK: find", testkey, find.count()
    name = models.TestsuiteName.objects.get(name=testsuite_name)
    return find.get(testsuite__name=name)


def remove(context, testsuite_name):
    """ Get or create a testplan in a certain order.

    @param context Testplan context organizes testplans in a logical group.
                   Testplans with the same context are in the same group.
                   The order indicates the order of the testplan in the
                   context.
    @param testsuite_name The testsuite name for the testplan
    """

    from testdb.models import Testplan
    from testdb.models import Context

    (context, _) = Context.objects.get_or_create(name=context)
    testplan = Testplan.objects.get(testsuite__context=context,
                                    testsuite__name__name=testsuite_name)
    testplan.delete()
    return True
