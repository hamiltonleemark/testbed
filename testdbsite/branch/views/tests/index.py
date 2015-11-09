from django.shortcuts import render_to_response
from testdb import models
from testdb import builds

class ViewRow(object):
    def __init__(self, order, plan, testsuite, test):
        """Contruct a product view. """
        self.order = order 
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


    product = models.TestProduct.objects.get(id=pid)
    testplan_name = product.key_get("testplan", None)
    testplan_name = models.Testplan.context_get(testplan_name)
    testplan_context = models.Context.objects.get(name=testplan_name)

    ##
    # Retrieve the test plan.
    # To view a products specific test plan. Retrieve the product and then
    # retrieve the testplan value.
    planorders = {}

    print "MARK: context", testplan_context
    print "MARK: testplan", models.Testplan.objects.all()

    testplan = models.Testplan.objects.get(context=testplan_context)

    testplans = testplan.testplanorder_set.order_by("order")
    order = 1
    for plan in testplans:
        testsuites = plan.testsuite_set.filter(context=testplan.context)

        for testsuite1 in testsuites:
            for test1 in testsuite1.test_set.all().order_by("name"):
                key = (testsuite1.name.name, test1.name.name)
                print "MARK: key", key
                planorders[key] = ViewRow(order, plan, testsuite1, test1)
                order += 1
    ##

    ##
    # retrieve build list.
    product_key = models.KVP.objects.get(key__value="product",
                                        value=str(product.product.value))
    branch_key = models.KVP.objects.get(key__value="branch",
                                        value=product.branch.value)
    blist = builds.filter(product_key, branch_key)

    context = models.Context.objects.get(name=context)
    results = {}

    for testplan in testplans:
        for buildid in blist:
            testsuites = testplan.testsuite_set.filter(context=context,
                                                       keys=buildid)
            for testsuite1 in testsuites:
                for test1 in testsuite1.test_set.all():
                    key = (buildid.value, testsuite1.name.name,
                           test1.name.name)
                    results[key] = test1.status

    planorders = [(item.order, item) for item in planorders.values()]
    planorders.sort()
    planorders = [item[1] for item in planorders]

    html_data = {
        # \todo retrieve this from the testplan.
        "results": results,
        "product": product,
        "headers": ["key1", "key2"],
        "planorders": planorders,
        "builds": blist
        }
    return render_to_response("tests/index.html", html_data)
