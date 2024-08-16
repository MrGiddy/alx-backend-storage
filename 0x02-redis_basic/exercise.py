#!/usr/bin/env python3
"""Implements a simple cache using Redis DB"""
import redis
import uuid
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """records the number of times a Cache instance method is called"""
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        key = method.__qualname__
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(key, 1)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """stores a function's history of inputs and outputs"""
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        inputs_key = f'{method.__qualname__}:inputs'
        outputs_key = f'{method.__qualname__}:outputs'
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(inputs_key, str(args))
            self._redis.rpush(outputs_key, output)
        return output
    return wrapper


def replay(method: Callable) -> None:
    """displays the history of calls of a function"""
    if method is None or not hasattr(method, '__self__'):
        return
    # Make keys for inputs and outputs lists
    inputs_key = f'{method.__qualname__}:inputs'
    outputs_key = f'{method.__qualname__}:outputs'
    # Retrieve the inputs and outputs from db
    instance = method.__self__
    redis_client = instance._redis
    if not isinstance(redis_client, redis.Redis):
        return
    inputs = redis_client.lrange(inputs_key, 0, -1)
    outputs = redis_client.lrange(outputs_key, 0, -1)
    # Display how many times method was called
    meth_qual_name = method.__qualname__
    method_calls = instance.get_int(meth_qual_name)
    print(f'{meth_qual_name} was called {method_calls} times:')
    # Iterate over input and output and display them
    for i, o in zip(inputs, outputs):
        input_tuple = i.decode('utf-8')
        output_val = o.decode('utf-8')
        print(f'{meth_qual_name}(*{input_tuple}) -> {output_val}')


class Cache():
    """Represents a cache object"""

    def __init__(self) -> None:
        """instantiates a Cache"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """stores cache data into a Redis DB"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Callable = None
            ) -> Union[str, bytes, int, float]:
        """
        retrieves data from a Redis DB,
        converts the data to the desired format and returns it
        """
        data = self._redis.get(key)
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        retreives data from Redis DB,
        calls `get` to convert it to string,
        and returns it
        """
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        retreives data from Redis DB,
        converts it to int and returns it
        """
        return self.get(key, fn=lambda d: int(d))
