"""
Common database api for builds.
"""
import logging
from testdb import models

CONTEXT = "build.default"


# pylint: disable=W0622
def filter(product_key, branch_key=None):
    """ Return the list builds given the parameters. """

    logging.info("list build %s %s", product_key.value,
                 branch_key.value if branch_key else "*")
    (context, _) = models.Context.objects.get_or_create(name=CONTEXT)
    find = models.Testsuite.objects.filter(context=context, keys=product_key)

    if branch_key:
        find = find.filter(keys=branch_key)

    return [item.key_get("build") for item in find]
