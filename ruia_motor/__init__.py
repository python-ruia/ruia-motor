#!/usr/bin/env python
"""
 Created by howie.hu at 2019/2/14.
"""
from types import MethodType

from ruia import Spider

from ruia_motor.motor_base import MotorBase


class RuiaMotorInsert:
    """
    A Ruia plugin that uses the motor to insert data
    """

    def __init__(self, db: str = None, *, collection: str, data: dict):
        """
        Define parameters
        Motor doc: https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_collection.html#motor.motor_asyncio.AsyncIOMotorCollection.insert_one
        :param db:
        :param collection:
        :param data:
        """
        self.db = db
        self.collection = collection
        self.data = data

    @staticmethod
    async def process(spider_ins, callback_result):
        """
        Handle the insert operation by using motor
        :param spider_ins:
        :param callback_result:
        :return:
        """
        db = callback_result.db or spider_ins.mongodb_config["db"]
        collection = callback_result.collection
        data = callback_result.data

        coll_conn = spider_ins.motor_base.get_collection(db=db, collection=collection)

        try:
            await coll_conn.insert_one(document=data)
            # spider_ins.logger.info(f'<RuiaMotor: Insertsuccessful>')
        except Exception as e:
            spider_ins.logger.error(f"<RuiaMotor: Insert error {e}>")


class RuiaMotorUpdate:
    """
    A Ruia plugin that uses the motor to update data
    """

    def __init__(
        self,
        db: str = None,
        *,
        collection: str,
        filter: dict,
        update: dict,
        upsert: bool = False,
    ):
        """
        Define parameters
        Motor doc: https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_collection.html#motor.motor_asyncio.AsyncIOMotorCollection.update_one
        :param db:
        :param collection:
        :param filter: A query that matches the document to update.
        :param update: The modifications to apply.
        :param upsert: If True, perform an insert if no documents match the filter.
        """
        self.db = db
        self.collection = collection
        self.filter = filter
        self.update = update
        self.upsert = upsert

    @staticmethod
    async def process(spider_ins, callback_result):
        """
        Handle the insert operation by using motor
        :param spider_ins:
        :param callback_result:
        :return:
        """
        db = callback_result.db or spider_ins.mongodb_config["db"]
        collection = callback_result.collection
        filter = callback_result.filter
        update = callback_result.update
        upsert = callback_result.upsert

        coll_conn = spider_ins.motor_base.get_collection(db=db, collection=collection)

        try:
            await coll_conn.update_one(filter=filter, update=update, upsert=upsert)
        except Exception as e:
            spider_ins.logger.error(f"<RuiaMotor: Update error {e}>")


def init_spider(*, spider_ins: Spider):
    """
    Ruia configuration initialization
    :param spider_ins:
    :return:
    """
    mongodb_config = getattr(spider_ins, "mongodb_config", None)
    if not mongodb_config or not isinstance(mongodb_config, dict):
        raise ValueError(
            """
        RuiaMotor must have a param named mongodb_config, eg: 
        mongodb_config = {
            'username': '',
            'password': '',
            'host': '127.0.0.1',
            'port': 27017,
            'db': 'ruia_motor'
        }
        """
        )

    spider_ins.motor_base = MotorBase(
        mongodb_config=mongodb_config, loop=spider_ins.loop
    )
    spider_ins.callback_result_map = spider_ins.callback_result_map or {}
    # Insert
    spider_ins.process_insert_callback_result = MethodType(
        RuiaMotorInsert.process, spider_ins
    )
    spider_ins.callback_result_map.update(
        {"RuiaMotorInsert": "process_insert_callback_result"}
    )
    # Update
    spider_ins.process_update_callback_result = MethodType(
        RuiaMotorUpdate.process, spider_ins
    )
    spider_ins.callback_result_map.update(
        {"RuiaMotorUpdate": "process_update_callback_result"}
    )
