#!/usr/bin/env python3
"""Contains the definition of `list_all` function"""


def list_all(mongo_collection):
    """
    Lists all documents in a collection
    mongo_collection : A pymongo object
    """
    return [doc for doc in mongo_collection.find()]
