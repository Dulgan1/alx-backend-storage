#!/usr/bin/env python3
"""Module update"""


def update_topics(mongo_collection, name, topics):
    """updates documenst's (school's) topics"""
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})


