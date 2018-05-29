import ujson
from scrapy import Spider
from scrapy.http import FormRequest
from ..items import WeiboItem


def gen_card_group(cards):
    for card in cards:
        card_group = card.get('card_group')
        if card_group:
            yield card_group


def gen_mblog(card_groups):
    for card_group in card_groups:
        for item in card_group:
            mblog = item.get('mblog')
            if mblog:
                yield mblog


class WeiboKeywordSearchSpider(Spider):
    name = 'weibokeywordsearch'
    allowed_domains = ['m.weibo.cn']

    def __init__(self, *, query, settings, upper_bound=100):
        super(WeiboKeywordSearchSpider, self).__init__(settings=settings)
        self.api = 'https://m.weibo.cn/api/container/getIndex'
        self.containerid = '100103type=1&q={}'.format(query)
        self.upper_bound = upper_bound

    def start_requests(self):
        yield from (FormRequest(
            method='GET',
            url=self.api,
            formdata={'containerid': self.containerid, 'page': str(i)},
            meta={'page': i},
            callback=self.parse)
            for i in range(1, self.upper_bound + 1))

    def parse(self, response):
        result = ujson.loads(response.text)
        cards = result.get('data', {}).get('cards')
        if cards:
            current_page = response.meta['page']
            if current_page >= self.upper_bound:
                page = current_page + 1
                yield FormRequest(
                    method='GET',
                    url=self.api,
                    formdata={'containerid': self.containerid,
                              'page': str(page)},
                    meta={'page': page},
                    callback=self.parse)

            card_groups = gen_card_group(cards)
            mblogs = gen_mblog(card_groups)
            yield from (WeiboItem(itemid=mblog.get('id'), mblog=mblog)
                        for mblog in mblogs)
