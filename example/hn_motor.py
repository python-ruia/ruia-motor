#!/usr/bin/env python

from ruia import AttrField, Item, Response, Spider, TextField

from ruia_motor import RuiaMotorInsert, RuiaMotorUpdate, init_spider


class HackerNewsItem(Item):
    target_item = TextField(css_select="tr.athing")
    title = TextField(css_select="a.storylink")
    url = AttrField(css_select="a.storylink", attr="href")

    async def clean_title(self, value):
        return value.strip()


class HackerNewsSpider(Spider):
    start_urls = ["https://news.ycombinator.com/news?p=1"]
    aiohttp_kwargs = {"proxy": "http://0.0.0.0:1087"}

    async def parse(self, response: Response):
        async for item in HackerNewsItem.get_items(html=await response.text()):
            # Update data
            # https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_collection.html#motor.motor_asyncio.AsyncIOMotorCollection.update_one
            yield RuiaMotorUpdate(
                collection="hn_demo",
                filter={"title": item.title},
                update={"$set": item.results},
                upsert=True,
            )
            # Insert data
            # https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_collection.html#motor.motor_asyncio.AsyncIOMotorCollection.insert_one
            # yield RuiaMotorInsert(collection="hn_demo", data=item.results)


async def init_plugins_after_start(spider_ins):
    spider_ins.mongodb_config = {"host": "127.0.0.1", "port": 27017, "db": "ruia_motor"}
    init_spider(spider_ins=spider_ins)


if __name__ == "__main__":
    HackerNewsSpider.start(after_start=init_plugins_after_start)
