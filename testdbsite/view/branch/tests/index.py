from django.shortcuts import render_to_response
from testdb import models
from testdb import builds

class View(object):
    def __init__(self, order, testsuite, test):
        """Contruct a product view. """
        self.order = order
        self.testsuite = testsuite
        self.test = test

        # \todo consider removing this.
        testkeys = self.testsuite.testsuitekeyset_set.all()
        self.keys = [item.testkey for item in testkeys]

def view(request, pid):
    """ Summarize product information. """

    context = request.GET.get("context", "default")
    context = models.Testplan.context_name_get(context)

    product = models.TestProduct.objects.get(id=pid)
    testplan = product.key_get("testplan", None)

    ##
    # To view a products specific test plan. Retrieve the product and then
    # retrieve the testplan value.
    planorders = []
    try:
        testplans = models.Testplan.objects.get(context__name=context)
        for (order, testsuite1) in testplans.testsuites_all():
            for test in testsuite1.test_set.all():
                planorders += [View(order, testsuite, item)
                               for item in testplans.testsuites_all()]
    except models.Testplan.DoesNotExist:
        planorders = []

    ##
    # retrieve build list.
    product_key = models.TestKey.objects.get(key__value="product",
                                             value=str(product.product.value))
    branch_key = models.TestKey.objects.get(key__value="branch",
                                            value=product.branch.value)
    blist = builds.filter(product_key, branch_key)

    html_data = {
        # \todo retrieve this from the testplan.
        "product": product,
        "headers": ["key1", "key2"],
        "planorders": planorders,
        "builds": blist
        }
    return render_to_response("branch/tests/index.html", html_data)
