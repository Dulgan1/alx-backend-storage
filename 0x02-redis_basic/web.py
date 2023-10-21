#!/usr/bin/env python3
"""Web request caching: redis"""
import requests
import redis

redis_c = redis.Redis()


def keep_count(fn: Callable) -> Callable:
    """Caches count of fn function call"""
    def wrapper(arg):
        key = 'count:' + arg
        redis_c.incr(key)
        redis_c.expire(key, 10)
        return fn(arg)
    return wrapper


@keep_count
def get_page(url: str) -> str:
    """Gets content of web page, caches count of webpage gets"""
    return requests.get(url).text
