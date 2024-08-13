import unittest
import time
import threading
import os
from lru import LRUCache  # Assuming the LRUCache class is in a file named lru_cache.py


class TestLRUCache(unittest.TestCase):

    def setUp(self):
        self.cache = LRUCache(capacity=3)

    def test_basic_put_get(self):
        self.cache.put("a", 1)
        self.cache.put("b", 2)
        self.cache.put("c", 3)
        self.assertEqual(self.cache.get("a"), 1)
        self.assertEqual(self.cache.get("b"), 2)
        self.assertEqual(self.cache.get("c"), 3)

    def test_lru_eviction(self):
        self.cache.put("a", 1)
        self.cache.put("b", 2)
        self.cache.put("c", 3)
        self.cache.put("d", 4)  # This should evict "a"
        self.assertIsNone(self.cache.get("a"))
        self.assertEqual(self.cache.get("b"), 2)
        self.assertEqual(self.cache.get("c"), 3)
        self.assertEqual(self.cache.get("d"), 4)

    def test_update_existing_key(self):
        self.cache.put("a", 1)
        self.cache.put("b", 2)
        self.cache.put("a", 3)  # Update value for "a"
        self.assertEqual(self.cache.get("a"), 3)
        self.cache.put("c", 4)
        self.cache.put("d", 5)  # This should evict "b"
        self.assertIsNone(self.cache.get("b"))

    def test_ttl_expiration(self):
        self.cache.put("a", 1, ttl=1)
        self.cache.put("b", 2)
        time.sleep(2)
        self.assertIsNone(self.cache.get("a"))  # "a" should be expired
        self.assertEqual(self.cache.get("b"), 2)

    def test_ttl_update(self):
        self.cache.put("a", 1, ttl=4)  # Set TTL to 4 seconds
        time.sleep(1)  # Wait for 1 second, still within TTL
        self.cache.put("a", 2)  # Updating "a" should reset its TTL
        time.sleep(2)  # Wait for another 2 seconds, still within TTL
        self.assertEqual(self.cache.get("a"), 2)  # "a" should not have expired yet

    def test_thread_safety(self):
        def cache_operations():
            for i in range(10):
                self.cache.put(f"key{i}", i)
                time.sleep(0.01)
                self.cache.get(f"key{i}")

        threads = [threading.Thread(target=cache_operations) for _ in range(5)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # The cache should still operate correctly
        self.assertIn("key9", self.cache.cache)

    def test_persistence(self):
        self.cache.put("a", 1)
        self.cache.put("b", 2)
        self.cache.put("c", 3)
        self.cache.save_to_file('cache_test.pkl')

        new_cache = LRUCache(capacity=3)
        new_cache.load_from_file('cache_test.pkl')
        self.assertEqual(new_cache.get("a"), 1)
        self.assertEqual(new_cache.get("b"), 2)
        self.assertEqual(new_cache.get("c"), 3)

        # Clean up the test file
        os.remove('cache_test.pkl')

    def test_persistence_with_ttl(self):
        self.cache.put("a", 1, ttl=2)
        self.cache.put("b", 2)
        self.cache.save_to_file('cache_test_with_ttl.pkl')

        time.sleep(3)

        new_cache = LRUCache(capacity=3)
        new_cache.load_from_file('cache_test_with_ttl.pkl')
        self.assertIsNone(new_cache.get("a"))  # "a" should be expired
        self.assertEqual(new_cache.get("b"), 2)

        # Clean up the test file
        os.remove('cache_test_with_ttl.pkl')


if __name__ == '__main__':
    unittest.main()
