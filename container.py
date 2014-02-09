
class Container(object):

    def set(self, key, data):
        """ Adds data identified by the key"""
        raise NotImplementedError

    def get(self, key):
        """ 
        Get the data identified by the key
        Returns None if not key (miss), returns the data if found (hit)
        """
        raise NotImplementedError

    def rm(self, key):
        """Deletes the data identified by the key"""
        raise NotImplementedError

    def get_all(self):
        """Gets all the data ina  dict format"""
        raise NotImplementedError


class SimpleContainer(Container):
    """Simple container is an abstraction of a regular dict"""

    def __init__(self):
        self._data = {}

    def set(self, key, data):
        self._data[key] = data

    def get(self, key):
        return self._data.get(key, None)

    def rm(self, key):
        del self._data[key]

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

    def rm(self, key):
        pass

    def get_all(self):
        pass