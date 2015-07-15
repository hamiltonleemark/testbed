import argparse

def add_subparser(subparser):
    """ Create testsuite CLI commands. """

    parser = subparser.add_parser("test")
    parser.add_argument("add", help="add a test")

    return subparser
    

