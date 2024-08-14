#!/usr/bin/env python3
"""insert a document"""


def insert_school(mongo_collection, **kwargs):
    """insert school"""
    res = mongo_collection.insert_one(kwargs)
    return res.inserted_id
