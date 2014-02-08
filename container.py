
class Container(object):

    def set(key, data):
        raise NotImplementedError
    def get(key):
        raise NotImplementedError


class SimpleContainer(Container):
    """Simple container is an abstraction of a regular dict"""
    def __init__(self):
        self._data = {}

    def set(self, key, data):
        self._data[key] = data

    def get(self, key):
        """ Returns None if not key (miss), returns the data if found (hit)"""
        return self._data.get(key, None)

class LRUContainer(Container):
    """LRU container"""
    def __init__(self):
        pass

    def set(self, key, data):
        pass

    def get(self, key):
        pass