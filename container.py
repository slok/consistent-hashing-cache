
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

    def __init__(self, max_entries):
        self._max = max_entries
        self._linked_list = []
        self._data = {}

    def set(self, key, data):
        # Insert at the front of the list
        self._linked_list.insert(0, key)        
        self._data[key] = data

        # Check if there is space left
        if len(self._linked_list) > self._max:
            self._remove_oldest()

    def get(self, key):
        if not len(self._linked_list):
            return None
        else:
            data = self._data.get(key, None)
            if data:
                # hit, so data to front
                self._linked_list.remove(key)
                self._linked_list.insert(0, key)

            return data

    def rm(self, key):
        self._linked_list.remove(key)
        del self._data[key]

    def _remove_oldest(self):
        key = self._linked_list.pop()
        del self._data[key]

    def get_all(self):
        return self._data

