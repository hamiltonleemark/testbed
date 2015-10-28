from django.shortcuts import render_to_response
from testdb import models
from testdb import builds

class View(object):
    def __init__(self, planorder):
        """Contruct a product view. """
        self.order = planorder[0]
        self.testsuite = planorder[1]

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
    try:
        testplans = models.Testplan.objects.get(context__name=context)
        planorders = [View(item) for item in testplans.testsuites_all()]
    except models.Testplan.DoesNotExist:
        planorders = []

    # \todo product should hold TestKeys not keys
    product_key = models.KVP.objects.get(key__value="product",
                                         value=str(product.product.value))
    branch_key = models.KVP.objects.get(key__value="branch",
                                        value=product.branch.value)
    ##
    # retrieve build list.
    blist = builds.filter(product_key, branch_key)

    html_data = {
        # \todo retrieve this from the testplan.
        "product": product,
        "headers": ["key1", "key2"],
        "planorders": planorders,
        "builds": blist
        }
    return render_to_response("branch/testsuites/index.html", html_data)
