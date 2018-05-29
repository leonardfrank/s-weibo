from twisted.internet import reactor
from twisted.internet import defer
from twisted.internet import task

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from s_weibo.spiders.weibo import WeiboKeywordSearchSpider


@defer.inlineCallbacks
def crawl(mappings, settings):
    for (coll_name, keyword) in mappings:
        settings.update({'MONGO_COLLECTION': coll_name})
        yield runner.crawl(WeiboKeywordSearchSpider,
                           query=keyword, settings=settings)
    # reactor.stop()


if __name__ == '__main__':
    inter_val = 60 * 30
    mappings = (('lancome', '兰蔻'), ('estee_lauder', '雅诗兰黛'))

    configure_logging()
    settings = get_project_settings()
    settings.update({'LOG_LEVEL': 'INFO'})
    runner = CrawlerRunner(settings)

    listener = task.LoopingCall(crawl, mappings, settings)
    listener.start(inter_val)

    reactor.run()
