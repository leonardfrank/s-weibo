from scrapy import Item
from scrapy import Field


class WeiboItem(Item):
    itemid = Field()
    mblog = Field()
