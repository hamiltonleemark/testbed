#!/usr/bin/python
"""
Single entry point for test bed CLI.
"""
import os
import sys
import logging

LOGGER = logging.getLogger("")


def parse():
    """ main entry point. """
    from testbed.core import commands

    arg_parser = commands.main()
    args = arg_parser.parse_args()
    commands.args_process(args)


def main():
    """ Main entry point. """
    # \todo figure out how this works when we install tbd.
    try:
        testbed_dir = os.environ["TESTBED"]
    except KeyError:
        ##
        # This script is also a template. When this script is installed
        # {{TESTBED }} is set to a path.
        installation = "{{TESTBED}}"
        if installation[0] == "{":
            cur_dir = os.path.abspath(os.path.join("..", __file__))
            testbed_dir = os.path.dirname(cur_dir)
        else:
            testbed_dir = installation

    sys.path.append(testbed_dir)
    return parse()

# pylint: disable=W0703
if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception, arg:
        LOGGER.error(arg)
