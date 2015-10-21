"""
Common database api for builds.
"""
import logging
from testdb import models

CONTEXT = "build.default"


# pylint: disable=W0622
def filter(product_key, branch_key=None, history=10):
    """ Return the list builds given the parameters.

    Build list is returned in newest to oldest.
    """

    logging.info("list build %s %s", product_key.value,
                 branch_key.value if branch_key else "*")
    (context, _) = models.Context.objects.get_or_create(name=CONTEXT)
    find = models.Testsuite.objects.filter(context=context, keys=product_key)
    find = find.order_by("-timestamp")

    if branch_key:
        find = find.filter(keys=branch_key)

    return [item.key_get("build") for item in find[0:history]]
