#!/usr/bin/env python3
"""Web request caching: redis"""
import requests
import redis

redis_c = redis.Redis()


def get_page(url: str) -> str:
    """Gets content of web page, caches count of webpage gets"""
    key = 'count:{{}}'.format(url)
    redis_c.incr(key)
    redis_c.expire(key, 10)
    return requests.get(url).text
