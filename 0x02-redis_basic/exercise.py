#!/usr/bin/env python3
"""Cache module"""
import redis
import uuid
from typing import Union


class Cache:
    """Caching system class"""

    def __init__(self):
        """Initializes and instance with a redis client"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[float, int, str, bytes]) -> str:
        """Stores data with key value through redis client instance
        as cache, returns key"""
        obj_jey: uuid.UUID = uuid.uuid4()
        self._redis.set(str(obj_key), data)

        return str(obj_key)
