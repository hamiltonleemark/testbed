"""
 A hierarchy of dictionaries.
"""


# pylint: disable=R0903
class DataTree(object):
    """ A tree of dictionaries. """
    def __init__(self):
        self.root = {}

    def add(self, path, value):
        """ Add value given the path. """

        root = self.root
        for item in path[:-1]:
            next_level = root.get(item, {})
            root[item] = next_level
            root = next_level

        root[path[-1]] = value
        return value
