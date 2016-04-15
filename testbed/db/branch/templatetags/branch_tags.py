from django import template
from testdb import models

register = template.Library()

@register.simple_tag(takes_context=True, name="view_cell")
def view_cell(context, build, testsuite, test):

    key = (build, testsuite, test)
    print "MARK: view_cell 1", key
    results = context["results"]
    status = results.get(key, models.Test.UNKNOWN)
    return models.Test.status_to_str(status, True)

@register.simple_tag(takes_context=True, name="view_td_cell")
def view_td_cell(context, build, testsuite, test):


    key = (build, testsuite, test)
    print "MARK: view_td_cell 1", key
    results = context["results"]
    status = results.get(key, models.Test.UNKNOWN)
    print "MARK: status", status

    status_code = models.Test.status_to_str(status, True)
    status_code = "" if status_code is None else status_code
    style = models.Test.status_to_str(status)
    return '<td class="%s">%s</td>' % (style, status_code)
