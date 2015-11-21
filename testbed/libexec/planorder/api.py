"""
Functionality common to more than one command.
"""


# /todo testplan_name should be optional parameter.
def get(testplan_name, testsuite_name, testkeys):
    """ Return TestPlanOrder given testsuite name and corresponding keys. """

    from testdb import models

    name = models.TestsuiteName.objects.get(name=testsuite_name)
    find = models.TestplanOrder.objects.filter(testsuite__name=name)

    if testplan_name:
        testplan_name = models.Testplan.context_get(testplan_name)
        find = find.filter(testplan__context=testplan_name)

    # \todo deal with many test plan or zero.
    for (key, value) in testkeys:
        testkey = models.KVP.get(key=key, value=value)
        find = find.filter(testsuite__keys=testkey)

    if find.count() == 0:
        raise models.TestplanOrder.DoesNotExist(
            "testplan %s does not exist" % testplan_name)

    return find.first()
