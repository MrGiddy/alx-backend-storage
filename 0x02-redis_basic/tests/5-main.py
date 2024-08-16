#!/usr/bin/env python3
import redis

redis_client = redis.Redis()

get_page = __import__('web').get_page

url = 'http://www.github.com'
get_page(url)

print(redis_client.get(f'count:{url}'))
