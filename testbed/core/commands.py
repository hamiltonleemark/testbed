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
LOGGER.setLevel(logging.DEBUG)

class VerbositySet(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(VerbositySet, self).__init__(option_strings, dest, nargs,
                                           **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        """ Called when verboaity. """

        LOGGER.setLevel(level=logging.DEBUG)



def argparser():
    """ Create top level argument parser. """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--verbose', '-v', required=False, nargs='?',
                            action=VerbositySet, const=logging.DEBUG,
                            help="enable debug verbosity.")
    return arg_parser


def onerror(name):
    """ Show module that fails to load. """
    LOGGER.error("importing module %s" % name)
    _, _, traceback = sys.exc_info()
    print_tb(traceback)


def extensions_find(arg_parser):
    """ Look for command extensions. """

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
            module.argparser(arg_parser)
            
    

def main():
    arg_parser = argparser()
    extensions_find(arg_parser)
    return arg_parser
