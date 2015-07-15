import argparse

def argparser(root_argparse):
    """ Create testsuite CLI commands. """

    subparser = root_argparse.add_subparsers(help="testsuite commands")
    parser = subparser.add_parser("testsuite")
    parser.add_argument("add", help="add a testsuite")
    parser.add_argument("remove", help="remove a testsuite")

    return root_argparse
    
    
