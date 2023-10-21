#!/usr/bin/env python3
"""Web request caching: redis"""
import requests
import redis

def get_page(url: str) -> str:
    """Gets content of web page, caches count of webpage gets"""
    redis_c = redis.Redis()
    key = 'count:' + url
    response = requests.get(url).text
    redis_c.incr(key)
    redis_c.expire(key, 10)
    
    return response
