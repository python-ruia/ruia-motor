#!/usr/bin/env python

from ruia import AttrField, TextField, Item, Spider
from ruia_motor import RuiaMotor


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')

    async def clean_title(self, value):
        return value.strip()


class HackerNewsSpider(Spider):
    start_urls = ['https://news.ycombinator.com/news?p=1', 'https://news.ycombinator.com/news?p=2']

    async def parse(self, response):
        async for item in HackerNewsItem.get_items(html=response.html):
            yield RuiaMotor(collection='hn_demo', data=item.results)


async def init_plugins_after_start(spider_ins):
    spider_ins.mongodb_config = {
        'host': '127.0.0.1',
        'port': 27017,
        'db': 'ruia_motor'
    }
    RuiaMotor.init_spider(spider_ins=spider_ins)


if __name__ == '__main__':
    HackerNewsSpider.start(after_start=init_plugins_after_start)
