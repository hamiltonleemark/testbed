from django.shortcuts import render_to_response
from testdb import models
from testdb import builds

class View(object):
    order = 1
    
    def __init__(self, plan, testsuite, test):
        """Contruct a product view. """
        self.order = View.order
        View.order += 1
        self.plan = plan
        self.testsuite = testsuite
        self.test = test
        self.results = []

        # \todo consider removing this.
        testkeys = self.testsuite.testsuitekeyset_set.all()
        self.keys = [item.testkey for item in testkeys]

def view(request, pid):
    """ Summarize product information. """

    context = request.GET.get("context", "default")
    context = models.Context.objects.get(name=context)

    product = models.TestProduct.objects.get(id=pid)
    testplan_name = product.key_get("testplan", None)

    ##
    # Retrieve the test plan.
    # To view a products specific test plan. Retrieve the product and then
    # retrieve the testplan value.
    planorders = {}

    testplan_context = models.Testplan.context_get(testplan_name)
    testplan = models.Testplan.objects.get(context=testplan_context)

    testplans = testplan.testplanorder_set.order_by("order")
    for plan in testplans:
        testsuites = plan.testsuite_set.filter(context=testplan.context)
        for testsuite1 in testsuites:
            for test1 in testsuite1.test_set.all():
                key = (testsuite1.name.name, test1.name.name)
                planorders[key] = View(plan, testsuite1, test1)

    ##

    ##
    # retrieve build list.
    product_key = models.KVP.objects.get(key__value="product",
                                             value=str(product.product.value))
    branch_key = models.KVP.objects.get(key__value="branch",
                                            value=product.branch.value)
    blist = builds.filter(product_key, branch_key)

    for testplan in testplans:
        for buildid in blist:
            testsuites = testplan.testsuite_set.filter(context=context,
                                                       keys=buildid)
            for testsuite1 in testsuites:
                for test1 in testsuite1.test_set.all():
                    key = (testsuite1.name.name, test1.name.name)
                    planorders[key].results.append(test1.status)

    planorders = [(item.order, item) for item in planorders.values()]
    planorders.sort()
    planorders = [item[1] for item in planorders]

    html_data = {
        # \todo retrieve this from the testplan.
        "product": product,
        "headers": ["key1", "key2"],
        "planorders": planorders,
        "builds": blist
        }
    return render_to_response("branch/tests/index.html", html_data)
