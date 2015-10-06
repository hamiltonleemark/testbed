"""
Serialize API.
"""
from django.core import serializers


class Serializer(object):
    """
    Recursively serializes testbed instances.

    Django's default serialize interface does not recursively serialize
    foreign objects. Only the foreign primary key is serialized. This
    implementation handles recursively traversing foreign objects and
    serializes them if the object has not already been serialized. The
    primary key and obj.__class__.__name__ are used to prevent
    duplicate instances from being serialized.

    Normal operation is to call Serializer.add() for each model instance
    and their foreign instances then ending with a call to
    Serializer.serialize().
    """
    def __init__(self, hdl, serialize_format, indent):
        self._hdl = hdl
        self._format = serialize_format
        self._indent = indent
        self._prev_results = set()
        self._results = []

    def add(self, item):
        """ Add content to be serialized. """
        key = (item.__class__.__name__, item.pk)
        if key not in self._prev_results:
            self._results.append(item)
            self._prev_results.add(key)

    def serialize(self):
        """ Serialize a django object. """
        serializers.serialize(self._format, self._results, indent=self._indent,
                              stream=self._hdl)
