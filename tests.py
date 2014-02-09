
import unittest

from ring import ConsistentRing
from container import SimpleContainer, LRUContainer

class TestConsintentHashing(unittest.TestCase):

    def setUp(self):
        #Simplify the hash function
        self.hash_function = lambda x: int(x)

    def test_hashing_add(self):
        """Checks the hashing works ok"""

        node_keys = ("1", "3", "5") # will be: 1, 3, 5, 11, 13, 15, 21, 23, 25
        test_data = {
            "0": "1",
            "2": "3",
            "5": "5",
            "7": "1",
            "11": "1",
            "13": "3",
            "14": "5",
            "15": "5",
            "16": "1",
            "21": "1",
            "22": "3",
            "24": "5",
        }

        # Create a new ring, yay!
        ring = ConsistentRing(self.hash_function, 3)

        # Add our nodes
        ring.add(*node_keys)

        # Get the keys and check if it returns the proper node

        for k,v in test_data.items():
            self.assertEqual(ring.get(k), v)

    def test_hashing_delete(self):
        """Checks the hashing works ok"""

        node_keys = ("1", "3", "5") # will be: 1, 3, 5, 11, 13, 15, 21, 23, 25
        test_data = {
            "0": "1",
            "2": "5",
            "5": "5",
            "7": "1",
            "11": "1",
            "13": "5",
            "14": "5",
            "15": "5",
            "16": "1",
            "21": "1",
            "22": "5",
            "24": "5",
        }

        # Create a new ring, yay!
        ring = ConsistentRing(self.hash_function, 3)

        # Add our nodes
        ring.add(*node_keys)

        # Remove node 3
        ring.remove("3")

        # Get the keys and check if it returns the proper node

        for k,v in test_data.items():
            self.assertEqual(ring.get(k), v)

    def test_consistency(self):
        """Checks that two different rings have the same behavior"""
        
        # Make 2 rings
        ring1 = ConsistentRing()
        ring2 = ConsistentRing()

        # Set nodes
        ring1.add("node1", "node2", "node3", "node4", "node5")
        ring2.add("node4", "node2", "node5", "node1", "node3")

        # Check the result is the same in both nodes
        for i in range(1000):
            self.assertEqual(ring1.get(str(i)), ring2.get(str(i)))


class TestSimpleContainer(unittest.TestCase):

    def setUp(self):
        self.test_data = {
            "Batman": "Bruce Wayne",
            "Spiderman": "Peter Parker",
            "Superman": "Clark Ken",
        }

    def test_hashing_hit(self):
        c = SimpleContainer()

        for k, v in self.test_data.items():
            c.set(k, v)

        for k,v in self.test_data.items():
            self.assertEqual(c.get(k), v)

    def test_remove_data(self):
        c = SimpleContainer()

        for k, v in self.test_data.items():
            c.set(k, v)

        self.assertEqual(len(c.get_all()), len(self.test_data))
        c.rm("Superman")
        self.assertEqual(len(c.get_all()), len(self.test_data) - 1)

class TestLRUContainer(unittest.TestCase):

    def setUp(self):
        self.test_data = {
            "Batman": "Bruce Wayne",
            "Spiderman": "Peter Parker",
            "Superman": "Clark Ken",
            "Iron man": "Tony Stark",
        }

    def test_cache_max(self):
        max_limit = 3
        c = LRUContainer(max_limit)

        for k, v in self.test_data.items():
            c.set(k, v)

        self.assertEqual(len(c.get_all()), max_limit)

    def test_storing(self):
        c = LRUContainer(4)

        for k, v in self.test_data.items():
            c.set(k, v)

        for k,v in self.test_data.items():
            self.assertEqual(c.get(k), v)

    def test_hashing_hit(self):
        c = LRUContainer(3)

        c.set("Spiderman", self.test_data["Spiderman"])
        c.set("Batman", self.test_data["Batman"])
        c.set("Superman", self.test_data["Superman"])

        # Hits
        c.get("Batman")
        c.get("Spiderman")

        # superman should go out and not spiderman (First inser order)
        c.set("Iron man", self.test_data["Iron man"])
        self.assertIsNone(c.get("Superman"))



if __name__ == '__main__':
    unittest.main()