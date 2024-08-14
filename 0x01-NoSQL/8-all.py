#!/usr/bin/env python3
"""List all documents"""


def list_all(mongo_collection):
    """list documents"""
    return [document for document in mongo_collection.find()]
