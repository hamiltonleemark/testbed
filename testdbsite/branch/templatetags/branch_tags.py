from django import template

register = template.Library()

@register.simple_tag(takes_context=True, name="view_cell")
def view_cell(context, build, testsuite, test):

    key = (build, testsuite, test)
    results = context["results"]
    return results.get(key, "")
