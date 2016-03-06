#!/usr/bin/python
"""
Single entry point for test bed CLI.
"""
import os
import sys
import logging


def parse():
    """ main entry point. """
    from testbed.core import commands

    arg_parser = commands.main()
    args = arg_parser.parse_args()
    return commands.args_process(args)


def env_setup():
    """ Main entry point.

    If calling tbd from within a .git clone append the appropriate
    testbed directory clone otherwise python content is stored
    under the normal site-packages.
    """

    ##
    # If the git directory exists, at this location then this script
    # is part of a git clone.
    git_dir = os.path.abspath(os.path.join(__file__, "..", "..", ".git"))
    if os.path.exists(git_dir):
        logging.info("add working directory content to PYTHONPATH.")

        ##
        # This path is necessary to load anything under testbed clone.
        testbed_dir = os.path.abspath(os.path.join(__file__, "..", ".."))
        sys.path.insert(0, testbed_dir)


# pylint: disable=W0703
if __name__ == "__main__":
    try:
        env_setup()
        # pylint: disable=C0413
        from testbed.core import database

        database.init()
        sys.exit(parse())
    except Exception, arg:
        logging.exception(arg)
        sys.exit(1)
