#!/usr/bin/python
"""
CLI for testbd.
"""
import os
import sys
import logging
import argparse

LOGGER = logging.getLogger(__name__)


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
        cur_dir = os.path.abspath(os.path.join("..", __file__))
        testbed_dir = os.path.dirname(cur_dir)
    LOGGER.debug("appending %s to path" % testbed_dir)
    sys.path.append(testbed_dir)
        
    sys.exit(main())
                       

