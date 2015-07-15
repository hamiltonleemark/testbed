#!/usr/bin/python
"""
Single entry point for test bed CLI.
"""
import os
import sys
import logging
import argparse


LOGGER = logging.getLogger("")


def main():
    """ main entry point. """
    from testbed.core import commands

    arg_parser = commands.main()
    args = arg_parser.parse_args()

if __name__ == "__main__":
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
    sys.exit(main())
