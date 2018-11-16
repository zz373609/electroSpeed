# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from spider_ban.items import ProductItem
from scrapy.exceptions import DropItem


class MongoPipeline(object):
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_db = mongo_db
        self.mongo_uri = mongo_uri

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'banggood')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, ProductItem):
            self.db['product'].insert_one(dict(item))
        return item


class DuplicatesPipeline(object):
    def __init__(self):
        self.ids_seen_product = set()
    
    def process_item(self,item,spider):
        if isinstance(item,ProductItem):
            _id = item['_id']
            if _id in self.ids_seen_product:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.ids_seen_product.add(_id)
                return item
        return item



