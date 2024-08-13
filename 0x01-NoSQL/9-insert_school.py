#!/usr/bin/env python3
"""Contains the definition of `insert_school` function"""


def insert_school(mongo_collection, **kwargs):
    """inserts a new document in a collection based on kwargs"""
    feedback = mongo_collection.insert_one(kwargs)
    return feedback.inserted_id
