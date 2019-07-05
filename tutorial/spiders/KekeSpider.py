# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from tutorial.items import TutorialItem
from datetime import *
import os
import re
from bs4 import BeautifulSoup

class KekeSpider(scrapy.spiders.Spider):

    # print 'scrapy runspider KekeSpider.py'
    name = 'kekenet'
    allowed_domains = ['kekenet.com']
    start_urls = []

    def __init__(self, category=None, *args, **kwargs):
        super(KekeSpider, self).__init__(*args, **kwargs)
        self.start_urls.append('http://www.kekenet.com/read/pic/')
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
        self.start_urls.append('http://www.kekenet.com/Article/duwu/')
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
        self.start_urls.append('http://www.kekenet.com/broadcast/voaspecial/')
        self.start_urls.append('http://www.kekenet.com/broadcast/Normal/')
        self.start_urls.append('http://www.kekenet.com/broadcast/BBC/')
        self.start_urls.append('http://www.kekenet.com/broadcast/CNN/')
        self.start_urls.append('http://www.kekenet.com/broadcast/foxnews/')
        self.start_urls.append('http://www.kekenet.com/broadcast/NPR/')
        self.start_urls.append('http://www.kekenet.com/broadcast/Science/')
        self.start_urls.append('http://www.kekenet.com/broadcast/APnews/')
        self.start_urls.append('http://www.kekenet.com/broadcast/PBS/')
        self.start_urls.append('http://www.kekenet.com/broadcast/NBC/')
        self.start_urls.append('http://www.kekenet.com/Article/media/economist/')
        self.start_urls.append('http://www.kekenet.com/video/tv/')
        self.start_urls.append('http://www.kekenet.com/video/movie/')
        self.start_urls.append('http://www.kekenet.com/video/englishplay/')
        self.start_urls.append('http://www.kekenet.com/Article/videolis/video/')
        self.start_urls.append('http://www.kekenet.com/word/')
        # for i in range(290,250,-1):
        #     self.start_urls.append('http://www.kekenet.com/kouyu/original/List_%d.shtml' % i)

    def parse(self, response):
        print 'scrapy parse:'+response.url

        sel = Selector(response)
        if 'word' in response.url:
            sites = sel.xpath('//ul[@class="list_box_2_new"]/li')
        else:
            sites = sel.xpath('//ul[@id="menu-list"]/li')
        for site in sites:
            item = TutorialItem()
            if 'kouyu' in response.url:
                item['type_name'] = u'英语口语'
                item['category'] = u'spoken_english'
                item['source_url'] = site.xpath('h2/a[2]/@href').extract()[0]
            elif 'Article' in response.url or 'broadcast' in response.url or 'video' in response.url:
                item['type_name'] = u'英语听力'
                item['category'] = u'listening'
                item['source_url'] = site.xpath('h2/a[2]/@href').extract()[0]
            elif 'word' in response.url:
                item['type_name'] = u'英语词汇'
                item['category'] = u'word'
                item['source_url'] = 'http://www.kekenet.com/' + site.xpath('h2/a[2]/@href').extract()[0]
            elif 'read' in response.url:
                item['type_name'] = u'双语阅读'
                item['category'] = u'shuangyu_reading'
                if 'work' in response.url or 'Economics' in response.url or 'Sports' in response.url or 'keji' in response.url:
                    item['source_url'] = site.xpath('h2/a/@href').extract()[0]
                elif 'culture' in response.url or 'politics' in response.url or 'entertainment' in response.url or 'shehui' in response.url or 'economy' in response.url:
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
                imgthumburl = img[0]
                if "_" in imgthumburl:
                    filefullname = os.path.basename(imgthumburl)
                    dir = os.path.dirname(imgthumburl)
                    imgurls = filefullname.split('_')
                    imgthumburl =  dir + "/" +imgurls[len(imgurls)-1]
                item['img_url'] = imgthumburl
            else:
                item['img_url'] = ''
            print item['title'].encode('utf-8')
            print item['source_url']
            yield scrapy.Request(item['source_url'], self.parse_detail, meta={'item':item})

    def parse_detail(self,response):
        item = response.meta['item']
        img_urls = []
        info = ''
        sel = Selector(response)

        site = sel.xpath('//div[@class="info-qh"]')
        if site:
            infos = site.xpath('string(.)').extract()
            imgs = site.xpath('//div[@class="info-qh"]//img/@src').extract()
            if len(imgs) > 0:
                for im in imgs:
                    img_urls.append(im)
            info = infos[0].strip()
        else:
            site = sel.xpath('//div[@id="article"]')
            imgs1 = site.xpath('//div[@id="article"]//img/@src').extract()
            if len(imgs1) > 0:
                for im in imgs1:
                    img_urls.append(im)

            soup = BeautifulSoup(response.body, "html5lib")
            [script.extract() for script in soup.findAll('script')]
            [style.extract() for style in soup.findAll('style')]
            [span.extract() for span in soup.findAll('span',attrs={"style":"display:none"})]
            temp_content = soup.find('div', id='article').stripped_strings
            for con in temp_content:
                if con is None:
                    pass
                elif u'来源' in con or 'http://www.kekenet.com/' in con or u'请勿转载' in con:
                    pass
                elif len(con) == 0:
                    pass
                else:
                    info += con
                    info += u'\n\n'

        publish_time = site.xpath('//time/text()').extract()[0].encode('utf-8')[7:26]
        item['publish_time'] = datetime.strptime(publish_time, "%Y-%m-%d %H:%M:%S")

        type = 'text'
        media_url = ''
        if 'thunder_url ="' in response.body:
            media_start = response.body.index('thunder_url ="')
            if '.mp3";' in response.body:
                media_end = response.body.index('.mp3";', media_start)
                media_url = response.body[media_start + 14:media_end + 4]
                type = 'mp3'
                if "domain= '" in response.body:
                    domain_start = response.body.index("domain= '")
                    domain_end = response.body.index("';", domain_start)
                    domain_name = response.body[domain_start + 9:domain_end]
                    media_url = domain_name + media_url
                else:
                    media_url = 'http://k6.kekenet.com/' + media_url
                print '-----has mp3 player:'+media_url
            elif '.mp4";' in response.body:
                media_end = response.body.index('.mp4";', media_start)
                media_url = response.body[media_start + 14:media_end + 4]
                media_url = 'http://k6.kekenet.com/' + media_url
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

        pages_href = sel.xpath('//div[@id="contentText"]//ul/li/a/@href').extract()
        if len(pages_href) > 0:
            i = 1
            nextpages = "http://www.kekenet.com/" + pages_href[i]
            yield scrapy.Request(nextpages, self.parse_page, meta={'item': item,'pages_href':pages_href,'i':i})
        else:
            yield item

    def parse_page(self,response):
        pages_href = response.meta['pages_href']
        i = response.meta['i']
        i += 1
        img_urls = []
        item = response.meta['item']
        info = item['content']
        img_urls = item['img_urls']

        soup = BeautifulSoup(response.body, "html5lib")
        [script.extract() for script in soup.findAll('script')]
        [style.extract() for style in soup.findAll('style')]
        [span.extract() for span in soup.findAll('span', attrs={"style": "display:none"})]
        article = soup.find('div', id='article')
        imgs = article.find_all('img')
        if len(imgs) > 0:
            for img in imgs:
                img_urls.append(img['src'])
        temp_content = article.get_text()
        # for con in temp_content:
        #     if con is None:
        #         pass
        #     elif u'来源' in con or 'http://www.kekenet.com/' in con or u'请勿转载' in con or u'译文为可可英语翻译' in con:
        #         pass
        #     elif u'。' == con or '.' == con or u'？' == con or '?' == con:
        #         pass
        #     elif len(con) == 0:
        #         pass
        #     else:
        #         info += con
        #         info += u'\n'
        info += temp_content
        item['content'] = info
        item['img_urls'] = img_urls
        if i < len(pages_href):
            nextpages = "http://www.kekenet.com/" + pages_href[i]
            yield scrapy.Request(nextpages, self.parse_page, meta={'item': item,'pages_href':pages_href,'i':i})
        else:
            yield item