import argparse


def add_testsuite(args):
    """ Add a testsuite to the database. """
    print "MARK: args", args


def add_subparser(subparser):
    """ Create testsuite CLI commands. """

    parser = subparser.add_parser("testsuite")

    subparser = parser.add_subparsers()
    parser = subparser.add_parser("add",
                                  description="Add a testsuite",
                                  help="Add a testsuite.")
    parser.add_argument("name", type=str,
                        help="add a testsuite")
    parser.set_defaults(func=add_testsuite)
    parser = subparser.add_parser("remove")
    parser.add_argument("name", type=str,
                        help="add a testsuite")

    return subparser
