import argparse

def argparser():
    """ Create argument parser. """

    arg_parser = argparse.ArgumentParser()

    return arg_parser


def execute_commands(arg_parser):
    """ Handle execute arg parser. """

    arg_parser.parse()
    
