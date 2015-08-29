"""
Functionality common to more than one command.
"""
import logging

CONTEXT = "testplan.default"


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

    if order == -1:
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
