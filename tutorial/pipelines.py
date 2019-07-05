# -*- coding: utf-8 -*-
import leancloud
from leancloud import Object
from leancloud import Query
import datetime
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from tutorial.items import TutorialItem
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

itemId = 0

class TutorialPipeline(object):

    def __init__(self):
        global itemId
        leancloud.init('3fg5ql3r45i3apx2is4j9on5q5rf6kapxce51t5bc0ffw2y4', 'twhlgs6nvdt7z7sfaw76ujbmaw7l12gb8v6sdyjw1nzk9b1a')
        itemId = get_lastest_item_id()
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        print '-----init-----leancloud.init------itemId:%d' % itemId

    def process_item(self, item, spider):
        global itemId
        print '-----------------process_item-----------------------'
        if is_exit(item['title'],item['category']):
            print 'already exit'
            return item
        else:
            itemId += 1
            Composition = Object.extend('Reading')
            mComposition = Composition()
            mComposition.set('item_id', itemId)
            mComposition.set('title', item['title'])
            mComposition.set('img_url', item['img_url'])
            mComposition.set('content', item['content'])
            mComposition.set('type_name', item['type_name'])
            mComposition.set('publish_time', item['publish_time'])
            mComposition.set('type_id', item['type_id'])
            mComposition.set('source_url', item['source_url'])
            mComposition.set('source_name', item['source_name'])
            mComposition.set('category', item['category'])
            mComposition.set('type', item['type'])
            mComposition.set('img_type', 'url')
            mComposition.set('img_urls', item['img_urls'])
            mComposition.set('media_url', item['media_url'])
            mComposition.set('category_2', '')
            mComposition.save()
            print('save item')
            return item

    def spider_opened(self, spider):
        recordSpiderRunTime("kekespider start")

    def spider_closed(self, spider):
        recordSpiderRunTime("kekespider finish")

def is_exit(str, category):
    query = Query('Reading')
    query.equal_to('title', str)
    query.equal_to('category', category)
    querys = query.find()
    return len(querys) > 0

def get_lastest_item_id():
    query = Query('Reading')
    query.descending("item_id")
    query.limit(1)
    querys = query.find()
    if len(querys) == 0:
        return 0
    else:
        return querys[0].get("item_id")

def recordSpiderRunTime(str):
    now = datetime.datetime.now()
    ymd = now.strftime("%Y-%m-%d")
    run_time = now.strftime('%Y-%m-%d %H:%M:%S') + "  " + str

    SpiderRecord = Object.extend('SpiderRecord')
    mSpiderRecord = SpiderRecord()
    mSpiderRecord.set('ymd', ymd)
    mSpiderRecord.set('run_time', run_time)
    mSpiderRecord.save()
