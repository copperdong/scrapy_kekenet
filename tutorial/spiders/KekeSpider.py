# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from tutorial.items import TutorialItem
from bs4 import BeautifulSoup
from datetime import *
import time
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class KekeSpider(scrapy.spiders.Spider):

    print 'scrapy runspider KekeSpider.py'
    name = 'kekenet2'
    allowed_domains = ['kekenet.com']

    start_urls = []

    def __init__(self, category=None, *args, **kwargs):
        super(KekeSpider, self).__init__(*args, **kwargs)
        self.start_urls.append('http://www.kekenet.com/read/pic/')
        self.start_urls.append('http://www.kekenet.com/read/jy/')
        self.start_urls.append('http://www.kekenet.com/read/ss/')
        self.start_urls.append('http://www.kekenet.com/read/culture/')
        self.start_urls.append('http://www.kekenet.com/read/news/')
        self.start_urls.append('http://www.kekenet.com/read/news/work/')
        self.start_urls.append('http://www.kekenet.com/read/news/Economics/')
        self.start_urls.append('http://www.kekenet.com/read/news/Sports/')
        self.start_urls.append('http://www.kekenet.com/read/news/keji/')
        self.start_urls.append('http://www.kekenet.com/read/news/politics/')
        self.start_urls.append('http://www.kekenet.com/read/news/entertainment/')
        self.start_urls.append('http://www.kekenet.com/read/news/shehui/')
        self.start_urls.append('http://www.kekenet.com/read/news/economy/')
        self.start_urls.append('http://www.kekenet.com/read/story/')
        self.start_urls.append('http://www.kekenet.com/read/essay/')
        self.start_urls.append('http://www.kekenet.com/Article/chuji/')
        self.start_urls.append('http://www.kekenet.com/Article/practical/')
        self.start_urls.append('http://www.kekenet.com/Article/enjoy/')
        self.start_urls.append('http://www.kekenet.com/Article/kkspeech/')
        self.start_urls.append('http://www.kekenet.com/Article/media/')
        self.start_urls.append('http://www.kekenet.com/Article/yule/')
        self.start_urls.append('http://www.kekenet.com/Article/brand/')
        self.start_urls.append('http://www.kekenet.com/Article/jiaoxue/')
        self.start_urls.append('http://www.kekenet.com/kouyu/primary/')
        self.start_urls.append('http://www.kekenet.com/kouyu/bizoral/')
        self.start_urls.append('http://www.kekenet.com/kouyu/training/')
        self.start_urls.append('http://www.kekenet.com/kouyu/brand/')
        self.start_urls.append('http://www.kekenet.com/kouyu/hyoral/')
        self.start_urls.append('http://www.kekenet.com/kouyu/slang/')
        self.start_urls.append('http://www.kekenet.com/kouyu/original/')
        # for i in range(290,250,-1):
        #     self.start_urls.append('http://www.kekenet.com/kouyu/original/List_%d.shtml' % i)

    def parse(self, response):
        print 'scrapy parse:'+response.url

        sel = Selector(response)
        sites = sel.xpath('//ul[@id="menu-list"]/li')

        for site in sites:
            item = TutorialItem()
            if 'kouyu' in response.url:
                item['type_name'] = u'英语口语'
                item['category'] = u'spoken_english'
                item['source_url'] = site.xpath('h2/a[2]/@href').extract()[0]
            elif 'Article' in response.url:
                item['type_name'] = u'英语听力'
                item['category'] = u'listening'
                item['source_url'] = site.xpath('h2/a[2]/@href').extract()[0]
            elif 'read' in response.url:
                item['type_name'] = u'双语阅读'
                item['category'] = u'shuangyu_reading'
                if 'work' in response.url or 'Economics' in response.url or 'Sports' in response.url or 'keji' in response.url:
                    item['source_url'] = site.xpath('h2/a/@href').extract()[0]
                elif 'politics' in response.url or 'entertainment' in response.url or 'shehui' in response.url or 'economy' in response.url:
                    item['source_url'] = site.xpath('h2/a/@href').extract()[0]
                elif 'story' in response.url or 'essay' in response.url:
                    item['type_name'] = u'双语故事'
                    item['category'] = u'story'
                    item['source_url'] = site.xpath('h2/a[2]/@href').extract()[0]
                else:
                    item['source_url'] = site.xpath('h2/a[2]/@href').extract()[0]

            item['title'] = site.xpath('h2/a/text()').extract()[0]
            img = site.xpath('a/img/@src').extract()
            if img:
                item['img_url'] = img[0]
            else:
                item['img_url'] = ''
            print item['title'].encode('utf-8')
            print item['source_url']
            yield scrapy.Request(item['source_url'], self.parse_detail, meta={'item':item})

    def parse_detail(self,response):
        item = response.meta['item']
        img_urls = []
        sel = Selector(response)
        site = sel.xpath('//div[@class="info-qh"]')
        info = site.xpath('string(.)').extract()
        if info:
            imgs = site.xpath('//div[@class="info-qh"]//img/@src').extract()
            if len(imgs) > 0:
                for im in imgs:
                    img_urls.append(im)
            info = info[0].strip()
        else:
            site = sel.xpath('//div[@id="article"]')
            info = site.xpath('string(.)').extract()
            imgs1 = site.xpath('//div[@id="article"]//img/@src').extract()
            if len(imgs1) > 0:
                for im in imgs1:
                    img_urls.append(im)
            if info:
                info = info[0].strip()
            else:
                print '-----info is none'
                print site
                return

        publish_time = site.xpath('//time/text()').extract()[0].encode('utf-8')[7:26]
        item['publish_time'] = datetime.strptime(publish_time, "%Y-%m-%d %H:%M:%S")

        type = 'text'
        media_url = ''
        if 'thunder_url ="' in response.body:
            media_start = response.body.index('thunder_url ="')
            if '.mp3";' in response.body:
                media_end = response.body.index('.mp3";', media_start)
                media_url = response.body[media_start + 14:media_end + 4]
                media_url = 'http://k4.kekenet.com/' + media_url
                type = 'mp3'
                print '-----has mp3 player:'+media_url
            elif '.mp4";' in response.body:
                media_end = response.body.index('.mp4";', media_start)
                media_url = response.body[media_start + 14:media_end + 4]
                media_url = 'http://k4.kekenet.com/' + media_url
                type = 'video'
                print '-----has mp4 player:' + media_url

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


        item['content'] = info
        item['source_name'] = u'可可英语'
        item['type'] = type
        item['type_id'] = u'1016'
        item['img_urls'] = img_urls
        item['media_url'] = media_url

        yield item
