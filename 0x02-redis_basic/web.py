#!/usr/bin/env python3
"""Implements an expiring web cache and tracker"""
from datetime import timedelta
from functools import wraps
import redis
import requests
from typing import Callable


redis_client = redis.Redis()


def cache_page(method: Callable) -> Callable:
    """
    returns a cached webpage or calls `method` to fetch it
    then caches it with 10s expiry and returns it
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        # track the no. of times url is accessed
        redis_client.incr(f'count:{url}', 1)
        # check if the page's html is cached
        cached_page = redis_client.get(url)
        if cached_page:
            return cached_page.decode('utf-8')
        # fetch the page's html from the url
        page = method(url)
        # cache the html with an expiration
        redis_client.setex(url, timedelta(seconds=10), page)
        # return the fetched html
        return page
    return wrapper


@cache_page
def get_page(url: str) -> str:
    """obtains the HTML content of a particular URL and returns it"""
    resp = requests.get(url)
    return resp.text
