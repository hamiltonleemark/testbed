"""
Functionality common to more than one command.
"""
import logging

ROOT = "testplan"
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
    from testdb.models import TestsuiteName
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

    (name, _) = TestsuiteName.objects.get_or_create(name=testsuite_name)
    (testplanorder, created) = TestplanOrder.get_or_create(testplan, name,
                                                           order)
    return (testplan, created)


def planorder_get(context, testsuite_name, keys):
    """ Return TestplanOrder. """
    from testdb import models

    testkeys = [models.TestKey.get_or_create(key=key, value=value)[0]
                for (key, value) in keys if key != "build"]

    context = models.Context.objects.get(name=context)
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


def get(context, testkeys):
    """ Get testplan. """

    from testdb.models import Testplan
    from testdb.models import Context

    (context, _) = Context.objects.get_or_create(name=context)
    if len(testkeys) == 0:
         return Testplan.objects.get(context=context)
    else:
        find = Testplan.objects.filter(context=context)

        for testkey in testkeys[:-1]:
            find = find.filter(keys=testkey)
        return find.get(keys=testkeys[-1])

