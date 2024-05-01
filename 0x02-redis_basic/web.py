#!/usr/bin/python3
import requests
import redis

# Assuming the creation of a Redis connection as redis_conn
redis_conn = redis.Redis()

def get_page(url: str) -> str:
    cache_key = f"cache:{url}"
    count_key = f"count:{url}"
    
    # Increment the access count
    redis_conn.incr(count_key)
    
    # Try to get the cached content
    cached_content = redis_conn.get(cache_key)
    if cached_content:
        return cached_content.decode('utf-8')
    
    # Fetch the new content and cache it
    response = requests.get(url)
    redis_conn.setex(cache_key, 10, response.text)
    return response.text