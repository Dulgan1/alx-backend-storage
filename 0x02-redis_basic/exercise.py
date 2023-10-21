#!/usr/bin/env python3
"""Cache module"""
import redis
import uuid
from functools import wraps
from typing import Union, Callable


def call_history(method: Callable) -> Callable:
    """Decorator: saves call history of method"""
    key_input = method.__qaulname__ + ':input'
    key_output = method.__qualname__ + ':output'

    @wraps(method)
    def wrapper(self, *args, *kwargs):
        """Stores call data: inout and output"""
        self._redis.rpush(key_input, str(args))
        out_data = method(self, *args, **kwargs)
        self._redis.rpush(key_output, str(out_data))

        return out_data

    return wrapper

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
    @call_history
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
