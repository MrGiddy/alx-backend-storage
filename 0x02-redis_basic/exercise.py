#!/usr/bin/env python3
"""Writing strings to Redis"""
import redis
import uuid
from typing import Union, Callable


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

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float]:
        """
        retrieves data from a Redis DB,
        converts the data to the desired format and returns it
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
           data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        retreives data from Redis,
        converts it to string and returns it
        """
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        retreives data from Redis,
        converts it to int and returns it
        """
        return self.get(key, fn=lambda d: d.decode('utf-8'))
