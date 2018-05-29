from pymongo import MongoClient


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db, mongo_coll):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_coll = mongo_coll

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            mongo_uri=settings.get('MONGO_URI'),
            mongo_db=settings.get('MONGO_DATABASE', 'weibo'),
            mongo_coll=settings.get('MONGO_COLLECTION', 'result')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.coll = self.db[self.mongo_coll]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        result = dict(item)
        self.coll.update_one(
            {'_id': result['itemid']},
            {'$set': result['mblog']},
            upsert=True
        )
        return item
