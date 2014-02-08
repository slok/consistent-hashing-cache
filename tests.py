
import unittest

from consistenthashing import ConsistentRing

class TestConsintentHashing(unittest.TestCase):

    def setUp(self):
        #Simplify the hash function
        self.hash_function = lambda x: int(x)

    def test_hashing(self):
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


if __name__ == '__main__':
    unittest.main()