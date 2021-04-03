#!/usr/bin/env python
"""
 Created by howie.hu at 2019/2/14.
"""
import asyncio
from functools import wraps

from motor.motor_asyncio import AsyncIOMotorClient


def singleton(cls):
    """
    A singleton created by using decorator
    :param cls: cls
    :return: instance
    """
    _instances = {}

    @wraps(cls)
    def instance(*args, **kw):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kw)
        return _instances[cls]

    return instance


@singleton
class MotorBase:
    """
    About motor's doc: https://github.com/mongodb/motor
    """

    _db = {}
    _collection = {}

    def __init__(self, mongodb_config: dict, loop=None):
        self.mongodb_config = mongodb_config
        self.loop = loop or asyncio.get_event_loop()

    def client(self, db):
        motor_uri = "mongodb://{account}{host}:{port}/{database}".format(
            account="{username}:{password}@".format(
                username=self.mongodb_config["username"],
                password=self.mongodb_config["password"],
            )
            if self.mongodb_config.get("username")
            else "",
            host=self.mongodb_config.get("host", "localhost"),
            port=self.mongodb_config.get("port", 271017),
            database=db,
        )
        return AsyncIOMotorClient(motor_uri, io_loop=self.loop)

    def get_db(self, db=None):
        """
        Get a db instance
        :param db: database name
        :return: the motor db instance
        """
        db = db or self.mongodb_config["db"]
        if db not in self._db:
            self._db[db] = self.client(db=db)[db]

        return self._db[db]

    def get_collection(self, db=None, *, collection):
        """
        Get a collection instance
        :param db: database name
        :param collection: collection name
        :return: the motor collection instance
        """
        db = db or self.mongodb_config["db"]
        collection_key = db + collection
        if collection_key not in self._collection:
            self._collection[collection_key] = self.get_db(db)[collection]

        return self._collection[collection_key]
