#!/usr/bin/env python3
"""Cache module"""
import redis
import uuid
from functools import wraps
from typing import Union, Callable


def count_calls(method: Callable) -> Callable:
    """Decorator: counts calls on method"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Function wrapper"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """Caching system class"""

    def __init__(self):
        """Initializes and instance with a redis client"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores data with key value through redis client instance
        as cache, returns key"""
        obj_key: uuid.UUID = uuid.uuid4()
        self._redis.set(str(obj_key), data)

        return str(obj_key)

    def get(self, key: str, fn: Union[Callable, None] = None) \
            -> Union[float, int, str, bytes]:
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
