#!/usr/bin/env python3
"""Cache module"""
import redis
import uuid
from functools import wraps
from typing import Union, Callable


def call_history(method: Callable) -> Callable:
    """Decorator: saves call history of method"""
    key_input = method.__qualname__ + ':inputs'
    key_output = method.__qualname__ + ':outputs'

    @wraps(method)
    def wrapper(self, *args, **kwargs):
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

def replay(method: Callable) -> None:
    key = method.__qualname__
    key_input = key + ':inputs'
    key_output = key + ':outputs'
    redis = method.__self__._redis
    count = redis.get(key).decode('UTF-8')
    input_list = redis.lrange(key_input, 0, -1)
    output_list = redis.lrange(key_output, 0, -1)
    io_list = list(zip(input_list, output_list))

    print("{} was called {} times:".format(key, count))

    for i, o in io_list:
        input, output = i.decode('UTF-8'), o.decode('UTF-8')
        print("{}(*{}) -> {}".format(key, input, output))



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
