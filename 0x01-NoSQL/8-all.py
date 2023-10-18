#!/usr/bin/env python3
"""Module lists all document in collection"""


def list_all(mongo_collection):
    """Returns all documents in collection passed as argument"""
    if not mongo_collection:
        return []
    return [doc for doc in mongo_collection.find()]
