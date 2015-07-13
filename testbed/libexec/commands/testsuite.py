import argparse
def argparser(root_argparse):
    """ Create testsuite CLI commands. """

    testsuite_parser = argparse.ArgumentParser()
    sub_parser = argparse.ArgumentParser(help="sub-commands help",
                                         dst="subparser_name")
    sub_parser.arg_argument("testsuite", help = "Testsuite commands.")
    
    
