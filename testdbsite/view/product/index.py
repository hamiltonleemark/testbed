from django.shortcuts import render_to_response
from testdb import models

class ProductView(object):
    def __init__(self, product):
        """Contruct a product view. """
        self.product = product

    def id(self):
        """ Return the name of the product. """
        return str(self.product.id)

    def context(self):
        """ Return the name of the product. """
        return str(self.product.testsuite.context.name)

    def name(self):
        """ Return the name of the product. """
        return str(self.product.testsuite.name)

    def branch(self):
        """ Return the name of the product branch. """
        return str(self.product.testsuite.key_get("branch"))

def view(_):
    """ Summarize product information. """

    testplans = models.Testplan.objects.filter(
        testsuite__context__name__startswith="product").order_by("order")

    products = [ProductView(item) for item in testplans]
    html_data = {"products": products}
    return render_to_response("products/index.html", html_data)

def view_product(_, pid):
    """ Summarize product information. """

    product = models.Testplan.objects.get(id=pid)

    testplan = product.key_get("testplan")
    print "MARK: testplan", testplan

    ##
    # To view a products specific test plan. Retrieve the product and then
    # retrieve the testplan value.
    testplans = models.Testplan.objects.get(testsuite__name__name=testplan)

    html_data = {}
    return render_to_response("products/index.html", html_data)
    
