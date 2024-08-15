#!/usr/bin/env python3
"""Writing strings to Redis"""
import redis
import uuid
from typing import Union


class Cache():
    """Represents a cache object"""

    def __init__(self) -> None:
        """instantiates a Cache"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """stores cache data into a Redis DB"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
