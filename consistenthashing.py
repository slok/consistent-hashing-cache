
import settings

class ConsistentRing(object):
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

        

    def get(self, key):
        """ Gets the closest node near the provided key(string)"""

        key_hash = self._hash(bytearray(key, "utf-8"))

        # look over the ring to get the appropiate node where the key should be
        for i in self._keys:
            if key_hash <= i:
                return self._hash_map[i]

        # This is a ring ;) this means we have return to the start point
    
        return self._hash_map[self._keys[0]]