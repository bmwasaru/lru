# lru

Python library for caching arbitrary data using the Least-Recently-Used (LRU) eviction strategy

## LRUCache class

### Initialization (__init__)
- The LRUCache is initialized with a specific capacity, defining the maximum number of items it can hold.
- An OrderedDict is used to store the cache items, which maintains the order of insertion. This order is used to determine which items are least recently used.

### Retrieving (get):
- The ```get``` method fetches the value associated with a key. If the key exists, it is moved to the end of the OrderedDict, marking it as recently used.
- If the key is not found, the method returns ```None```.

### Inserting (put):
- The `put` method inserts a new key-value pair into the cache. If the key already exists, its value is updated, and the key is moved to the end.
- If inserting the new item exceeds the cache's capacity, the first item (the least recently used) is removed using `popitem(last=False)`.

### Representation (__repr__):
- The __repr__ method provides a string representation of the cache’s current state, which is useful for debugging or display.

### Usage:
The LRUCache class can be used to cache results of expensive function calls or any data that benefits from caching.

### Time-based Expiration:
- Each item can have an optional TTL (in seconds) when added to the cache using the `put` method.
- Items with a TTL will be automatically evicted when they expire. The `_evict_expired_items` method handles this cleanup.

### Thread Safety:
- All critical operations (`get`, `put`, `_evict_expired_items`, `save_to_file`, and `load_from_file`) are wrapped in a Lock to prevent race conditions when accessing the cache from multiple threads.

### Persistence:
- The `save_to_file method` saves the current cache state and TTLs to a file using pickle.
- The `load_from_file` method loads the cache and TTLs from a file and immediately evicts any expired items.

### Note:
- The TTL functionality is optional. If you don’t provide a TTL when putting an item, the item will remain in the cache until it is evicted due to the LRU policy.
- The `save_to_file` and `load_from_file` methods use `pickle`, which is suitable for simple persistence but not ideal for all use cases, especially if security or portability is a concern. Consider other serialization methods if needed.