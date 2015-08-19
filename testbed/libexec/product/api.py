"""
Functionality common to more than one command.
"""
import logging

CONTEXT = "product.default"


def get_or_create(product_name, branch_name, order):
    """ Get or create a testplan in a certain order.
    Order is just that the location of the testplan in the list of testplans.
    The order effects the location the testplan appears on web pages.
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
            order = find.order_by("-order")[0].order
        except IndexError:
            order = 1
        logging.info("using order %d", order)
    else:
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
    return Testplan.objects.get_or_create(testsuite=testsuite, order=order)


# pylint: disable=W0622
def filter(product_name=None, branch_name=None):
    """ Retrieve the list of products based on product and or branch_name. """

    from testdb.models import Testplan
    from testdb.models import Context
    from testdb.models import TestKey

    (context, _) = Context.objects.get_or_create(name=CONTEXT)
    find = Testplan.objects.filter(testsuite__context=context)
    if product_name:
        find = find.filter(testsuite__name__name=product_name)
    if branch_name:
        (branch_key, _) = TestKey.get_or_create("branch", branch_name)
        find = find.filter(testsuite__keys=branch_key)
    return find.order_by("-order")
