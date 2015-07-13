import sys
import logging
import inspect
import pkgutil
import argparse
import testbed.settings
import testbed.core.logger


LOGGER = testbed.core.logger.create(__name__)

class VerbositySet(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(VerbositySet, self).__init__(option_strings, dest, nargs,
                                           **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        """ Called when verboaity. """
        LOGGER.setLevel(logging.DEBUG)


def argparser():
    """ Create top level argument parser. """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--verbose', '-v', required=False, nargs='?',
                            action=VerbositySet, const=logging.DEBUG,
                            help="enable debug verbosity.")
    arg_parser.add_argument('--extension', '-e', dest="extension",
                            default=None, required=False, action='append',
                            help="provide alternate location for "
                                 "core functionality.")

    print "MARK: what"
    LOGGER.debug("debug")
    LOGGER.error("error")
    return arg_parser


def onerror(name):
    """ Show module that fails to load. """
    LOGGER.error("importing module %s" % name)
    _, _, traceback = sys.exc_info()
    print_tb(traceback)


def extensions_find(arg_parser):
    """ Look for command extensions. """

    for pkg in testbed.settings.COMMANDS:
        package = __import__(pkg)
        for package in pkgutil.walk_packages(package.__path__,
                                             package.__name__ + ".",
                                             onerror=onerror):
            _, package_name, _ = package
            LOGGER.debug("checking %s for command extensions" % package_name)
    

def main():
    arg_parser = argparser()
    extensions_find(arg_parser)
    return arg_parser
