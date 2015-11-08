"""
Functionality common to more than one command.
"""


def get(context, testsuite_name, keys):
    """ Return TestPlanOrder given testsuite name and corresponding keys. """

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


# pylint: disable=W0611
def get_or_create(context, testsuite_name, test_name, keys):
    """ Get or create testplan order. """
    from testdb import models

    print "MARK: get_or_create 1"
    testkeys = [models.KVP.get_or_create(key=key, value=value)[0]
                for (key, value) in keys]

    context = models.Testplan.context_get(context)
    find = models.Testplan.objects.filter(context=context)
    for testkey in testkeys:
        find = find.filter(keys=testkey)

    print "MARK: get_or_create 2"
    testplans = [item for item in find]
    if len(testplans) == 0:
        return (None, False)

    (name, _) = models.TestsuiteName.objects.get_or_create(name=testsuite_name)
    print "MARK: get_or_create 3"

    # \todo deal with many test plan or zero.
    (order, critem) = models.TestplanOrder.objects.get_or_create(
        testplan=testplans[0], testsuite__context=context,
        testsuite__name=name)
    print "MARK: get_or_create 4"

    for testsuite1 in order.testsuite_set.filter(context=context):
        (_, critem) = models.Test.get_or_create(testsuite1, test_name, [])
        return (order, critem)
    print "MARK: get_or_create 5"
    return (None, False)
