#!/usr/bin/env python3
"""Contains the definition of `nginx_logs_stats` function"""
from pymongo import MongoClient


def nginx_logs_stats(log_collections):
    """provides some stats about Nginx logs stored in MongoDB"""

    print(f'{log_collections.count_documents({})} logs')

    print('Methods:')

    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        count = log_collections.count_documents({"method": method})
        print(f'\tmethod {method}: {count}')

    count = log_collections.count_documents(
        {"method": "GET", "path": "/status"}
    )

    print(f'{count} status check')


def main():
    """Dviver code for the program"""
    client = MongoClient(host='localhost', port=27017)
    log_collections = client.logs.nginx
    nginx_logs_stats(log_collections)


if __name__ == '__main__':
    main()
