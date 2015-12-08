# (c) 2015 Mark Hamilton, <mark_lee_hamilton@att.net>
#
# This file is part of testbed
#
# Testbed is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Testbed is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Testdb.  If not, see <http://www.gnu.org/licenses/>.
"""
CLI for tests.
"""
import logging
import yaml


def do_add(args):
    """ Add a key value pair. """

    from testdb import models

    logging.info("adding kvp %s=%s", args.key, args.value)

    (key, created) = models.Key.objects.get_or_create(value=args.key)
    logging.debug("adding kvp %s created %s", key, created)

    (kvp, created) = models.KVP.objects.get_or_create(key=key,
                                                      value=args.value)
    logging.debug("adding kvp %s created %s", kvp, created)
    return True


def do_list(args):
    """ List KVP key value pairs. """

    from testdb import models

    if args.key:
        key = models.KVP.objects.get(value=args.key)
        kvps = models.KVP.objects.filter(key=key)
    else:
        kvps = models.KVP.objects.all().order_by("key")

    kvps = kvps.order_by("value")

    root = {}
    for kvp in kvps:
        key = str(kvp.key.value)
        if key in root:
            root[key]["value"].append(str(kvp.value))
        else:
            config_type = str(kvp.key.get_config_type_display())
            root[key] = {
                "type": config_type,
                "value": [str(kvp.value)]
                }

    print yaml.dump(root, default_flow_style=False)


def do_type(args):
    """ Set the KVP type to STRICT or ANY.

    Key Value Pairs (KVP) can either be STRICT or ANY. STRICT requires
    that all key and value pairs retrieved must exist in the database.
    This is a safety feature to prevent spelling mistakes from creating
    bogus key, value pairs. The concept of STRICT is not enforced with this
    CLI but with all other aspects of the database. ANY will create new key
    value pairs, if they do not already exist.
    """

    from testdb import models

    logging.info("adding kvp %s as %s", args.key, args.type)

    config_type = models.Key.str_to_config_type(args.type)
    models.Key.objects.update_or_create(value=args.key,
                                        defaults={"config_type": config_type})
    return True


def add_subparser(subparser):
    """ Create KVP CLI commands. """

    from testdb import models

    ##
    # Adding a test requires a testsuite.
    #
    # test add <testsuite> <name>
    parser = subparser.add_parser("kvp", help=__doc__)
    subparser = parser.add_subparsers()

    parser = subparser.add_parser("add", help="Add kvp key and value")
    parser.set_defaults(func=do_add)

    parser.add_argument("key", type=str, help="Name of key.")
    parser.add_argument("value", type=str, help="Product branch name.")

    parser = subparser.add_parser("list",
                                  description="List tests in their testsuit.",
                                  help="List test")
    parser.add_argument("--key", type=str, help="Name of product.")
    parser.set_defaults(func=do_list)

    choices = [item[1] for item in models.Key.CONFIG_TYPE]
    parser = subparser.add_parser("type", help="Add kvp key and value",
                                  description=do_type.__doc__)
    parser.add_argument("key", type=str, help="Name of key.")
    parser.add_argument("type", help="Set KVP type", choices=choices)
    parser.set_defaults(func=do_type)
    return subparser
