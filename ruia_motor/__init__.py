#!/usr/bin/env python
"""
 Created by howie.hu at 2019/2/14.
"""

from ruia_motor.motor_base import MotorBase


class RuiaMotor:

    def __init__(self, db=None, *, collection, data):
        self.db = db
        self.collection = collection
        self.data = data

    @classmethod
    def init_spider(cls, loop=None, *, spider):
        mongodb_config = getattr(spider, 'mongodb_config', None)
        if not mongodb_config or not isinstance(mongodb_config, dict):
            raise ValueError("""
            RuiaMotor must have a param named mongodb_config, eg: 
            mongodb_config = {
                'username': '',
                'password': '',
                'host': '127.0.0.1',
                'port': 27017,
                'db': 'ruia_motor'
            }
            """)

        spider.motor_base = MotorBase(mongodb_config=mongodb_config, loop=loop)
        spider.callback_result_map = spider.callback_result_map or {}
        setattr(spider, 'process_ruia_motor_callback_result', process_ruia_motor_callback_result)
        spider.callback_result_map.update({'RuiaMotor': 'process_ruia_motor_callback_result'})


async def process_ruia_motor_callback_result(spider_ins, callback_result: RuiaMotor):
    db = callback_result.db or spider_ins.mongodb_config['db']
    collection = callback_result.collection
    data = callback_result.data

    motor_base = spider_ins.motor_base
    coll_conn = motor_base.get_collection(db=db, collection=collection)

    try:
        await coll_conn.insert_one(document=data)
    except Exception as e:
        spider_ins.logger.error(f'<RuiaMotor: Insert error {e}>')
