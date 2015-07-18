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
import sys
import imp
import inspect
import os
import logging
import inspect
import importlib
import pkgutil
import argparse
import testbed.settings
import testbed.core.logger

console = logging.StreamHandler()
formatter = logging.Formatter(testbed.settings.FMT)
console.setFormatter(formatter)
LOGGER = logging.getLogger("")
LOGGER.addHandler(console)
LOGGER.setLevel(logging.INFO)

def args_process(args):
    """ Process any generic parameters. """

    if (args.verbose == 1):
        LOGGER.setLevel(level=logging.INFO)
        LOGGER.info("verbosity level set to INFO")
    elif (args.verbose > 1):
        LOGGER.setLevel(level=logging.DEBUG)
        LOGGER.info("verbosity level set to DEBUG")

    LOGGER.debug(args)

    args.func(args)

#class VerbositySet(argparse.Action):
    #def __init__(self, option_strings, dest, nargs=None, **kwargs):
        #super(VerbositySet, self).__init__(option_strings, dest, nargs,
                                           #**kwargs)
#
    #def __call__(self, parser, namespace, values, option_string=None):
        #""" Called when verboaity. """
#
        #LOGGER.setLevel(level=logging.DEBUG)
#

def argparser():
    """ Create top level argument parser. """
    arg_parser = argparse.ArgumentParser(prog="tbd")
    arg_parser.add_argument('--version', action="version",
                            version="%(prog)s 0.0.1")
    arg_parser.add_argument('--verbose', '-v', required=False, action="count",
                            help="enable debug verbosity.")
    return arg_parser


def onerror(name):
    """ Show module that fails to load. """
    LOGGER.error("importing module %s" % name)
    _, _, traceback = sys.exc_info()
    print_tb(traceback)


def extensions_find(arg_parser):
    """ Look for command extensions. """

    subparser = arg_parser.add_subparsers(title="subcommands",
                                          description="Valid subcommands",
                                          help="Each subcommands supports --help for additional information.")

    for package in testbed.settings.COMMANDS:
        LOGGER.debug("loading commands %s" % package)
        package = importlib.import_module(package)
        for _, module, ispkg in pkgutil.walk_packages(package.__path__,
                                                    package.__name__ + ".",
                                                    onerror=onerror):
            if ispkg:
                continue
            LOGGER.debug("  loading commands from %s" % module)
            module = importlib.import_module(module)
            try:
                module.add_subparser(subparser)
            except AttributeError, arg:
                ##
                # This means that the module is missing the add method.
                # All modules identified in settings to extend CLI
                # must have an add method
                LOGGER.error("adding subparser for %s.%s" % (package, module))
                LOGGER.exception(arg)
    

def main():
    arg_parser = argparser()
    extensions_find(arg_parser)
    return arg_parser
