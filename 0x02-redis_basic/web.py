#!/usr/bin/python3
"""doc doc module"""

import requests
import redis
from functools import wraps


# For example, the Redis server is running on localhost:6379
redis_client = redis.Redis(host='localhost', port=6379, db=0)


def count_url_accesses(func):
    """doc doc Decorator that counts how many times a URL has been accessed."""
    @wraps(func)
    def wrapper(url):
        # Increment the count each time a URL is accessed
        count_key = f"count:{url}"
        redis_client.incr(count_key)
        return func(url)
    return wrapper


@count_url_accesses
def get_page(url: str) -> str:
    """doc doc Fetches HTML content of URL with caching and access counting"""
    cache_key = f"cache:{url}"
    # Check if the cached version exists
    cached_content = redis_client.get(cache_key)
    if cached_content:
        return cached_content.decode('utf-8')

    # If not cached, fetch the content and cache it with a 10-second expiration
    response = requests.get(url)
    redis_client.setex(cache_key, 10, response.text)
    return response.text
