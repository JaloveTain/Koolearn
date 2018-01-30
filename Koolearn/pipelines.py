# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from pymongo import MongoClient
import json
from scrapy.contrib.pipeline.images import ImagesPipeline
import scrapy
from Koolearn.settings import IMAGES_STORE as images_store

class MongoPipeline(object):

    MONGO_IP = 'localhost'
    MONGO_PORT = 27017
    MONGO_DB_NAME = 'TiKu'
    MONGO_COLLECTION_NAME = 'Koolearn'

    def __init__(self):
        self.mongo_client = MongoClient(self.MONGO_IP, self.MONGO_PORT)
        self.mongo_db = self.mongo_client[self.MONGO_DB_NAME]
        self.mongo_collection = self.mongo_db[self.MONGO_COLLECTION_NAME]
    
    def process_item(self, item, spider):
        self.mongo_collection.save(dict(item))
        
        return item

    def close_spider(self, spider):
        self.mongo_client.close()


class ImagesPipeline(ImagesPipeline):
    
    def get_media_requests(self, item, info):
        image_link = item['question_img_link']
        if len(image_link) > 0:
            yield scrapy.Request('http:' + image_link)
        else:
            return item

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        os.rename(images_store + image_path[0], images_store + "full/" + item['question_img_link'].replace('/','').replace('.',''))
        print(results)
        return item

