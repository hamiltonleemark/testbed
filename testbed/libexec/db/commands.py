# (c) 2015 Mark Hamilton, <mark.lee.hamilton@gmail.com>
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
Provide status information useful for debugging installation and setup.
"""
import logging
import ConfigParser

LOGGER = logging.getLogger(__name__)


def default_file_fill(ddict, default_file):
    """ Read default_file option for mysql configuration.
    django 1.7 and newer supports confifiguration defined in a plain text
    file.
    """

    if not default_file:
        return ddict

    config = ConfigParser.RawConfigParser()
    config.read(default_file)

    for (key, value) in config.items("client"):
        key = key.upper()
        ddict[key] = value
    return ddict


def do_dbls(_):
    """ Add a test. """
    import djconfig

    print "databases"
    for (db_name, db_config) in djconfig.settings.DATABASES.items():

        db_options = db_config.get("OPTIONS", {})
        default_file = db_options.get("read_default_file", {})
        db_config = default_file_fill(db_config, default_file)

        engine = db_config.get("ENGINE")
        host = db_config.get("HOST", None)
        user = db_config.get("USER", None)
        if user and host:
            hostname = "%s@%s:" % (user, host)
        else:
            hostname = ""
        name = db_config.get("NAME", None)

        print "  %s: %s%s:%s" % (db_name, hostname, engine, name)


def do_dbcheck(_):
    """ Check that the installation is good. """

    import djconfig
    if "default" in djconfig.settings.DATABASES:
        print "default database found ... pass"
    else:
        print "default database found ... fail"
        return 1

    ##
    # It does not matter if there are any products. Mostly like this is
    # called just after installation. This is just a way to confirm
    # installation is correct because the model can connect to the database
    try:
        from testdb import models
        print "load models ... pass"
    except Exception:
        print "load models ... fail"
        return 1

    try:
        [item for item in models.Product.objects.all()]
        print "connect to database ... pass"
    except Exception:
        print "connect to database ... fail"
        return 1
    return 0


def add_subparser(subparser):
    """ Status CLI commands. """

    ##
    # Adding a test requires a testsuite.
    #
    # test add <testsuite> <name>
    parser = subparser.add_parser("db", help=__doc__)
    subparser = parser.add_subparsers()

    parser = subparser.add_parser("list",
                                  description="list databases",
                                  help="List all databases.")
    parser.set_defaults(func=do_dbls)

    parser = subparser.add_parser("check",
                                  description="list databases",
                                  help="List all databases.")
    parser.set_defaults(func=do_dbcheck)
    return subparser
