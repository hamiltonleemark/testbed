"""
Functionality common to more than one command.
"""
import logging


def get_or_create(context, testsuite_name, order):

    from testdb import models

    print "MARK: order", order
    if order == -1:
        print "MARK: args", order
        (context, _) = models.Context.objects.get_or_create(name=context)
        find = models.Testplan.objects.filter(testsuite__context=context)
        try:
            order = find.order_by("order")[0].order
        except IndexError:
            order = 1
        logging.info("using order %d" % order)

    (testsuite, _) = models.Testsuite.get_or_create(context, testsuite, None)
    return models.Testplan.objects.get_or_create(testsuite=testsuite,
                                                 order=order)
    
