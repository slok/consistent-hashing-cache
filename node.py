from container import SimpleContainer

class Node(object):
    """ Representation of a node (will amnage the container)"""

    def __init__(self, key, ring, container=SimpleContainer()):
        self.key = key
        self._ring = ring
        self._container = container

        # Self add to the ring
        self.add_node_to_ring(self.key)

    def get_data(self, key):
        """ Gets the data from this node"""
        print("Get key: '{0}'".format(key))
        return self._container.get(key)

    def set_data(self, key, data):
        """ Sets data in this node"""
        print("Set key: '{0}'".format(key))
        self._container.set(key, data)

    def get_all_data(self):
        """ Gets all the data from the node (whole cached objects)"""
        return self._container.get_all()

    def where(self, key):
        """ Gets the key/location of the node where the data is"""
        print("Asking where should be key: '{0}'".format(key))
        return self._ring.get(key)

    def add_node_to_ring(self, key):
        """ Adds a node to the ring"""
        print("Add node to ring: '{0}'".format(key))
        # TODO: Check format
        return self._ring.add(key)

    def rm_node_from_ring(self, key):
        """ Removes a node to the ring"""
        print("Remove node from ring: '{0}'".format(key))
        # TODO: Check format
        return self._ring.remove(key)

    def stats(self):
        host, port = self.key.split(":") 
        return {
            "key": self.key,
            "host": host,
            "port": port,
            "nodes": self._ring.stats(),
            "data": self._container.get_all()
        }

