#!/usr/bin/python
"""
CLI for testbd.
"""
import os
import sys


def argparse():
    """ Generate arg parser. """
 
    import cmd_parser
    cmd_parser.argparse()


if __name__ == "__main__":
    os.environ.setdefault("TESTBED_SETTINGS", "testdb.settings") 

    try:
        from testbed.core import commands
    except ImportError:
         dir_name_path = os.path.join(os.path.dirname(__file__),
                                      os.path.pardir, "lib")
         print "MARK: dir 1", dir_name_path
         print "MARK: dir 2", os.path.abspath(dir_name_path)
         sys.path.append(os.path.abspath(dir_name_path))
         import testbed
         from testbed.core import commands
    commands.argparser()
