#!/usr/bin/env python3
"""Contains the definition of `schools_by_topic` function"""


def schools_by_topic(mongo_collection, topic):
    """returns the list of school having a specific topic"""
    # schools = mongo_collection.find({'topics': {'$in': [topic]}})
    # return [doc for doc in schools]

    filter = {'topics': {'$elemMatch': {'$eq': topic}}}
    return [doc for doc in mongo_collection.find(filter)]
