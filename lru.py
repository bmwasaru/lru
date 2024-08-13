import time
import pickle
from collections import OrderedDict
from threading import Lock


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()
        self.ttl = {}
        self.lock = Lock()

    def _evict_expired_items(self):
        current_time = time.time()
        expired_keys = [key for key, expiration in self.ttl.items() if expiration < current_time]
        for key in expired_keys:
            self.cache.pop(key, None)
            self.ttl.pop(key, None)

    def get(self, key: str):
        with self.lock:
            self._evict_expired_items()
            if key not in self.cache:
                return None
            else:
                self.cache.move_to_end(key)
                return self.cache[key]

    def put(self, key: str, value: any, ttl: int = None):
        with self.lock:
            self._evict_expired_items()
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = value
            if ttl:
                self.ttl[key] = time.time() + ttl
            if len(self.cache) > self.capacity:
                oldest = next(iter(self.cache))
                self.cache.pop(oldest)
                self.ttl.pop(oldest, None)

    def save_to_file(self, file_path: str):
        with self.lock:
            with open(file_path, 'wb') as f:
                pickle.dump((self.cache, self.ttl), f)

    def load_from_file(self, file_path: str):
        with self.lock:
            with open(file_path, 'rb') as f:
                self.cache, self.ttl = pickle.load(f)
            # Evict expired items immediately after loading
            self._evict_expired_items()

    def __repr__(self):
        with self.lock:
            return f'{self.__class__.__name__}(capacity={self.capacity}, cache={list(self.cache.items())}, ttl={self.ttl})'
