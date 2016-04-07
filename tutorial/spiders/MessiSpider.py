# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from tutorial.items import TutorialItem
from bs4 import BeautifulSoup
from datetime import *
import time


class MessiSpider(scrapy.spiders.Spider):

    print 'start kekenet scrapy crawl kekenet'
    name = 'kekenet'
    allowed_domains = ['kekenet.com']

    start_urls = [
        'http://www.kekenet.com/read/pic/',
        'http://www.kekenet.com/read/jy/',
        'http://www.kekenet.com/read/ss/',
        'http://www.kekenet.com/read/news/work/',
        'http://www.kekenet.com/read/news/Economics/',
        'http://www.kekenet.com/read/news/Sports/',
        "http://www.kekenet.com/read/news/keji/",
        "http://www.kekenet.com/read/news/politics/",
        'http://www.kekenet.com/read/news/entertainment/',
        'http://www.kekenet.com/read/news/shehui/',
        'http://www.kekenet.com/read/news/economy/',
        'http://www.kekenet.com/read/essay/',
        "http://www.kekenet.com/read/culture/"
    ]
    def parse(self, response):
        print 'scrapy parse'

        sel = Selector(response)
        sites = sel.xpath('//ul[@id="menu-list"]/li')

        for site in sites:
            item = TutorialItem()
            item['title'] = site.xpath('h2/a/text()').extract()[0]
            item['source_url'] = site.xpath('h2/a/@href').extract()[0]
            img = site.xpath('a/img/@src').extract()
            if img:
                item['img_url'] = img[0]
            else:
                item['img_url'] = ''
            publish_time = site.xpath('p/text()').extract()[0][0:11]
            item['publish_time'] = datetime.strptime(publish_time+' 00:00:00', "%Y-%m-%d %H:%M:%S")
            print item['title'].encode('utf-8')
            yield scrapy.Request(item['source_url'], self.parse_detail, meta={'item':item})

    def parse_detail(self,response):
        item = response.meta['item']
        img_urls = []
        sel = Selector(response)
        site = sel.xpath('//div[@class="info-qh"]')
        info = site.xpath('string(.)').extract()
        if info:
            info = info[0].strip()
        else:
            print '-----info is none'
            print site
            return
        imgs = site.xpath('//div[@class="info-qh"]//img/@src').extract()

        trs = sel.xpath('//table[@class="wordList"]/tr')
        if trs:
            info += u'\n' + u'重点单词:' + u'\n'
            for tr in trs[1:]:
                if tr.xpath('./td[1]/span/a/text()').extract():
                    info += ''.join(tr.xpath('./td[1]/span/a/text()').extract()[0])
                    info += u'  '
                if tr.xpath('./td[2]/span/text()').extract():
                    info += ''.join(tr.xpath('./td[2]/span/text()').extract()[0])
                    info += u'  '
                if tr.xpath('./td[3]/div/div/p/text()').extract():
                    info += ''.join(tr.xpath('./td[3]/div/div/p/text()').extract()[0])
                    info += u'\n'
        else:
            print '-----tables is none'
            print trs

        if len(imgs) > 0:
            for im in imgs:
                img_urls.append(im)
        item['content'] = info
        item['source_name'] = u'可可英语'
        item['type_name'] = u'双语阅读'
        item['type'] = u'text'
        item['type_id'] = u'1015'
        item['category'] = u'shuangyu_reading'
        item['img_urls'] = img_urls
        yield item
