"""
Store database content based on filter.

Calling with --count not specified will show the number of items that
will be stored. This is a good way to see the impact of --keyvalue options.
"""

import os
import logging
import testbed.core.serializers


def do_store(args):
    """ Store content. """
    from testdb import models

    (dst_path, _) = os.path.split(args.dstfile)

    if not os.path.exists(dst_path):
        os.makedirs(dst_path)

    try:
        context = models.Context.objects.get(name=args.context)
        find = models.Testsuite.objects.filter(context=context)
        logging.info("Context %s limits results %d", args.context,
                     find.count())
    except models.Context.DoesNotExist:
        find = models.Testsuite.objects.all()
        logging.info("results %d", find.count())

    ##
    # Find appropriate testplan
    for value in args.filters:
        testkey = models.TestKey.objects.get(value=value)
        find = find.filter(testkey=testkey)

        # find = find.filter(testplanorder__testplan__testkey=testkey)
        logging.info("value %s limits results %d", value, find.count())

    ##
    # Assert at this point find points to a list of testsuites that must
    # be saved.

    ##
    # django does not support storing recursive objects. Instead
    # we need to figure out which foreign keys must be saved. Not
    # trivial since many objects can point to the same foreign object.
    # We need to.
    with open(args.dstfile, "w") as hdl:
        serializer = testbed.core.serializers.Serializer(hdl, "json", 2)
        for testsuite in find:
            testsuite.serialize(serializer)
        serializer.serialize()


def add_subparser(subparser):
    """ Create testsuite CLI commands. """

    parser = subparser.add_parser("store",
                                  help="Store database content to file.",
                                  description=__doc__)
    parser.add_argument("--context", default="default", type=str,
                        help="Specify a different context.")
    parser.set_defaults(func=do_store)
    parser.add_argument("dstfile", type=str,
                        help="Store database content into this file.")

    ##
    # List
    parser.add_argument("--filter", dest="filters", default=[],
                        action="append", help="Filter content")
    parser.add_argument("--count", default=0, type=int,
                        help="The number of testsuites to store in the"
                        "destination file.")

    return subparser
