"""
Functionality common to more than one command.
"""
import logging


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
    from testdb.models import Testsuite
    from testdb.models import Context

    if order == -1:
        (context, _) = Context.objects.get_or_create(name=context)
        find = Testplan.objects.filter(testsuite__context=context)
        try:
            order = find.order_by("-order")[0].order
        except IndexError:
            order = 1
        logging.info("using order %d", order)

    ##
    # Assert order is not -1.
    # Order is specified so now we have to move something.
    testplans = Testplan.objects.filter(order__gte=order).order_by("order")
    current_order = order
    for testplan in testplans:
        if testplan.order == current_order:
            testplan.order += 1
            testplan.save()
            current_order += 1
    (testsuite, _) = Testsuite.get_or_create(context, testsuite_name, None)
    return Testplan.get_or_create(testsuite=testsuite, order=order)
