# ruia-motor

A [Ruia](https://github.com/howie6879/ruia) plugin that uses the motor to store data


```text
Notice:  Works on ruia >= 0.5.0
```

### Installation

```shell
pip install -U ruia-motor
```

### Usage

`ruia-motor` will be automatically store data to mongodb:

```python
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
```

Enjoy it :)