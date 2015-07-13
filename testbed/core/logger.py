import argparse
import logging
import testbed.settings


def create(name):
    """ Create a logger. """
    logger = logging.getLogger(__name__)
    stream = logging.StreamHandler()
    logger.addHandler(stream)
    formatter = logging.Formatter(testbed.settings.FMT)
    stream.setFormatter(formatter)

    return logger
