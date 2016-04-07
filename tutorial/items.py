# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    source_url = scrapy.Field()
    img_url = scrapy.Field()
    publish_time = scrapy.Field()
    content = scrapy.Field()
    source_name = scrapy.Field()
    type_name = scrapy.Field()
    item_id = scrapy.Field()
    media_url = scrapy.Field()
    img_type = scrapy.Field()
    img_urls = scrapy.Field()
    type = scrapy.Field()
    category = scrapy.Field()
    type_id = scrapy.Field()

