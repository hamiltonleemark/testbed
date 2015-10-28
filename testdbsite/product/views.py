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
        return str(self.product.context.name)

    def name(self):
        """ Return the name of the product. """
        return str(self.product.product)

    def branch(self):
        """ Return the name of the product branch. """
        return str(self.product.branch)

def index(_):
    """ Summarize product information. """
    testplans = models.TestProduct.filter(None, None)

    products = [ProductView(item) for item in testplans]
    html_data = {"products": products}
    return render_to_response("product/index.html", html_data)

def index_product(_, pid):
    """ Summarize product information. """

    product = models.TestProduct.objects.get(id=pid)

    testplan = product.key_get("testplan", None)

    ##
    # To view a products specific test plan. Retrieve the product and then
    # retrieve the testplan value.
    try:
        testplans = models.Testplan.objects.get(context__name=testplan)
    except models.Testplan.DoesNotExist:
        testplans = []

    html_data = {}
    return render_to_response("product/index.html", html_data)
