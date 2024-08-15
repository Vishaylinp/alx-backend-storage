#!/usr/bin/env python3
"""list of school with specific topic"""


def schools_by_topic(mongo_collection, topic):
    """list school by topic"""
    topic_filter = {
        "topics": {
            "$elemMatch": {
                "$eq": topic,
            },
        },
    }
    return [document for document in mongo_collection.find(topic_filter)]
