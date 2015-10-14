"""
Common database api for builds.
"""
import logging
from testdb import models

CONTEXT = "build.default"


def build_list(product_name, branch_name=None):
    """ Return the list builds given the parameters. """

    logging.info("list build %s %s", product_name, branch_name)
    (context, _) = models.Context.objects.get_or_create(name=CONTEXT)
    find = models.Testsuite.objects.filter(context=context)

    if product_name:
        (product_key, _) = models.TestKey.get_or_create("product",
                                                        product_name)
        find = find.filter(keys=product_key)

    if branch_name:
        (branch_key, _) = models.TestKey.get_or_create("branch",
                                                       branch_name)
        find = find.filter(keys=branch_key)

    return [item.key_get("build") for item in find]
