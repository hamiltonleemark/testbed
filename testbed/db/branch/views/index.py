from django.shortcuts import render_to_response
from testdb import models
from testdb import builds

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

def view(_):
    """ Summarize product information. """

    testplans = models.Product.filter(None, None)

    products = [ProductView(item) for item in testplans]

    blist = builds.list(product.product, product.branch)

    html_data = {"products": products}
    return render_to_response("products/index.html", html_data)

def view(_, pid):
    """ Summarize product information. """

    product = models.Product.objects.get(id=pid)

    plans = product.key_get("testplan", None)

    plans = [item for item in plans.testsuites_all()] if plans else []

    html_data = {"plans" : plans}
    return render_to_response("products/index.html", html_data)
