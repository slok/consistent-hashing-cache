from container import SimpleContainer

class Node(object):
    """ Representation of a node (will amnage the container)"""

    def __init__(self, key, container=SimpleContainer()):
        self.key = key
        self._container = container

    def get(self, key):
        return self._container.get(key)

    def set(self, key, data):
        self._container.set(key, data)

    def get_all(self):
        return self._container.get_all()
