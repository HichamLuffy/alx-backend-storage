#!/usr/bin/env python3
"""exercise"""
import redis
import uuid
from functools import wraps
from typing import Callable, Optional, Union


def count_calls(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key
    
    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        value = self._redis.get(key)
        if value is not None and fn is not None:
            value = fn(value)
        return value
    
    def get_str(self, key: str) -> str:
        return self.get(key, fn=lambda x: x.decode('utf-8'))
    
    def get_int(self, key: str) -> int:
        return self.get(key, fn=int)

