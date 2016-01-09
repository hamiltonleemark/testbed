from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from testdb import models
from testdb import builds

class ViewRow(object):
    def __init__(self, hdr, order, plan, testsuite, test):
        """Contruct a product view. """
        self.order = order 
        self.plan = plan
        self.testsuite = testsuite
        self.test = test

        # \todo consider removing this.
        testkeys = [self.testsuite.value_get(item.value, "?") for item in hdr]
        self.keys = testkeys

def view(request, pid):
    """ Summarize product information. """

    print "MARK: view 1"

    context = request.GET.get("context", "default")
    history = request.GET.get("history", 10)

    product = models.Product.objects.get(id=pid)
    testplan_name = product.key_get("testplan", None)
    if not testplan_name:
        return render_to_response("tests/index.html", {})

    testplan_name = models.Testplan.context_get(testplan_name)
    testplan_context = models.Context.objects.get(name=testplan_name)

    ##
    # Retrieve the test plan.
    # To view a products specific test plan. Retrieve the product and then
    # retrieve the testplan value.
    planorders = {}

    testplan = models.Testplan.objects.get(context=testplan_context)

    keys = testplan.keys.all()

    testplans = testplan.testplanorder_set.order_by("order")
    print "MARK: testplans", testplans

    order = 1
    for plan in testplans:
        testsuites = plan.testsuite_set.filter(context=testplan.context)
        for testsuite1 in testsuites:
            for test1 in testsuite1.test_set.all().order_by("name"):
                key = (testsuite1.name.name, test1.name.name)
                planorders[key] = ViewRow(keys, order, plan, testsuite1, test1)
                order += 1
    ##

    ##
    # retrieve build list.
    product_key = models.KVP.objects.get(key__value="product",
                                         value=str(product.product.value))
    branch_key = models.KVP.objects.get(key__value="branch",
                                        value=product.branch.value)
    all_builds = builds.filter(product_key, branch_key)

    # Show history contacts per page
    paginator = Paginator(all_builds, history, request=request)

    ##
    # Generate pagination. The page url parameter is generated from the
    # code below. This is the standard django pagination functionality.
    try:
        page = request.GET.get('page', 1)
        buildids = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        buildids = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        buildids = paginator.page(paginator.num_pages)
    ##

    blist = [builds.BuildView(item) for item in buildids.object_list]
    
    results = {}
    try:
        context = models.Context.objects.get(name=context)
        for testplan in testplans:
            for buildid in blist:
                testsuites = testplan.testsuite_set.filter(context=context,
                                                           kvps=buildid.id)
                for testsuite1 in testsuites:
                    for test1 in testsuite1.test_set.all():
                        key = (buildid.id.value, testsuite1.name.name,
                               test1.name.name)
                        results[key] = test1.status
    
        planorders = [(item.order, item) for item in planorders.values()]
        planorders.sort()
        planorders = [item[1] for item in planorders]
    except models.Context.DoesNotExist:
        planorders = []

    html_data = {
        "results": results,
        "product": product,
        "headers": keys,
        "planorders": planorders,
        "builds": blist,
        "contacts": buildids
        }
    return render_to_response("tests/index.html", html_data)
