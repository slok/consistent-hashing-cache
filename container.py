
class Container(object):

    def set(self, key, data):
        raise NotImplementedError
    def get(self, key):
        raise NotImplementedError

    def get_all(self, ):
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

    def get_all(self):
        return self._data

class LRUContainer(Container):
    """LRU container"""
    def __init__(self):
        pass

    def set(self, key, data):
        pass

    def get(self, key):
        pass

    def get_all(self):
        pass