#!/usr/bin/env python3
"""Cache module"""
import redis
import uuid
from typing import Union, Callable


class Cache:
    """Caching system class"""

    def __init__(self):
        """Initializes and instance with a redis client"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[float, int, str, bytes]) -> str:
        """Stores data with key value through redis client instance
        as cache, returns key"""
        obj_key: uuid.UUID = uuid.uuid4()
        self._redis.set(str(obj_key), data)

        return str(obj_key)

    def get(self, key: str, fn: Callable) -> Union[float, int, str, bytes]:
        """gets stored data with key as key,
        uses fn to convert data from bytes to any"""
        data = self._redis.get(key)

        if fn:
            data = fn(data)

        return data

    def get_int(self, data: bytes) -> int:
        """Converts bytes data to int"""
        return int.from_bytes(data)

    def get_str(self, data: bytes) -> str:
        """Converts bytes data to str"""
        return str(data, 'UTF-8')
