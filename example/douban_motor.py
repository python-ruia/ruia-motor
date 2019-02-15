#!/usr/bin/env python

from ruia import AttrField, Item, Spider, TextField
from ruia_motor import RuiaMotor


class DoubanItem(Item):
    target_item = TextField(css_select='div.item')
    title = TextField(css_select='span.title')
    cover = AttrField(css_select='div.pic>a>img', attr='src')
    abstract = TextField(css_select='span.inq', default='')

    async def clean_title(self, title):
        if isinstance(title, str):
            return title
        else:
            return ''.join([i.text.strip().replace('\xa0', '') for i in title])


class DoubanSpider(Spider):
    start_urls = ['https://movie.douban.com/top250']

    mongodb_config = {
        'host': '127.0.0.1',
        'port': 27017,
        'db': 'ruia_motor'
    }

    async def parse(self, response):
        etree = response.html_etree
        pages = ['?start=0&filter='] + [i.get('href') for i in etree.cssselect('.paginator>a')]
        for index, page in enumerate(pages):
            url = self.start_urls[0] + page
            yield self.request(
                url=url,
                metadata={'index': index},
                callback=self.parse_item
            )

    async def parse_item(self, response):
        async for item in DoubanItem.get_items(html=response.html):
            data = item.results
            yield RuiaMotor(collection='douban250', data=data)


async def init_plugins_after_start(spider_ins):
    RuiaMotor.init_spider(spider_ins=spider_ins)


if __name__ == '__main__':
    DoubanSpider.start(after_start=init_plugins_after_start)
