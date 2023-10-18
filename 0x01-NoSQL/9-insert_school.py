#!/usr/bin/env python3
"""Module inserts new document to collection"""


def insert_school(mongo_collection, **kwargs):
    """Inserts and return the id of new docoument in collection"""
    doc = mongo_collection.insert_one(kwargs)
    return doc.inserted_id
