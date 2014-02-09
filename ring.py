
import settings

class Ring(object):

    def add(self, *keys):
        raise NotImplementedError

    def remove(self, *keys):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def empty(self, key):
        raise NotImplementedError


class ConsistentRing(Ring):
    """
        This class represents the ring of nodes managed with consistent hashing
        algorithm
    """
    
    def __init__(self, hash_func=settings.DEFAULT_HASH,
            replicas=settings.DEFAULT_REPLICAS):

        self._hash = hash_func # Contains the hashing function
        self._replicas = replicas # Contains the number of replicas per node
        self._keys = [] # A sorted list of hash keys (the ring with the node positions)
        self._hash_map = {} # our ring data (hash/value where value will be the node destination)
        # Yeah we could use a sorted dict but using a list is faster for sorting


    def __len__(self):
        return len(self._keys)

    def add(self, *keys):
        """ Adds keys (nodes) to the hash (ring)"""

        # Start adding each node
        for key in keys:
            # for each node add the number of replicas
            for i in range(self._replicas):
                # Calculate the hash of each replica
                replica_hash = self._hash(bytearray("{0}{1}".format(i, key),
                                                    "utf-8"))
                # Add the replica hash to the ordered list
                self._keys.append(replica_hash)

                # Each replica has its node key (destination)
                self._hash_map[replica_hash] = key


        # Sort the list (We will use this technique in ConsistentRing.get)
        self._keys.sort()

    
    def remove(self, *keys):
        """ Remove keys(nodes) to the hash (ring)"""

        for key in keys:
            # for each node remove the replicas
            for i in range(self._replicas):
                # Calculate the hash of each replica
                replica_hash = self._hash(bytearray("{0}{1}".format(i, key),
                                                    "utf-8"))
                # remove the replica hash from the ordered list
                self._keys.remove(replica_hash)

                del self._hash_map[replica_hash]


    def get(self, key):
        """ Gets the closest node near the provided key(string)"""

        if self.empty():
            return None

        key_hash = self._hash(bytearray(key, "utf-8"))

        # look over the ring to get the appropiate node where the key should be
        for i in self._keys:
            if key_hash <= i:
                return self._hash_map[i]

        # This is a ring ;) this means we have return to the start point
    
        return self._hash_map[self._keys[0]]

    def empty(self):
        return len(self) == 0