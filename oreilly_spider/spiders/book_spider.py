#coding=UTF-8
import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
import string
import re
import math
import urllib
from scrapy import log
from ..items import Book #this is the way to import code from parent directory
from ..items import BookSnippet
import os
#set default encoding
import sys
import time
#import pprint
from pprint import pprint
reload(sys)
sys.setdefaultencoding('utf-8')
#test
class BookSpider(scrapy.Spider):
    handle_httpstatus_list = [403,404]
    name = "oreillyspider"
    allowed_domains = ["oreilly.com"]
    start_urls = [
        #u'http://book.douban.com/tag/%E4%BA%92%E8%81%94%E7%BD%91?start=0&type=T'
        u'http://shop.oreilly.com/category/browse-subjects.do'
        #u'http://shop.oreilly.com/product/9781784393786.do'
        #u'http://book.douban.com/subject/1152912/'
    ]

    def parse(self, response):
        pprint(response)
        try:
            log.msg('start to parse url: '+str(response.url))
            if response.status == 403:
                time.sleep(10)
                log.msg("MISSED URL: "+str(response.url),level=log.WARNING)
                pass
            html_txt = response.body.decode("utf-8","ignore")
            hxs = Selector(text=html_txt)
            nav_area = hxs.xpath('//ul[@id="contextual-nav"]')
            items = nav_area.xpath('.//li[@role="menuitem"]/a/@href')
            if items:
                for item in items:
                    sub_url = item.extract()
                    log.msg('send out request for url: '+sub_url)
                    yield Request(url=sub_url,callback=self.parse_list)
            else:
                log.msg('no subcategory url found in start page',level=log.CRITICAL)
        except Exception,e:
            log.msg('failed to parse url: '+str(response.url))
            log.msg(str(e))
            raise

    def parse_list(self, response):
        try:
            if response.status == 403:
                time.sleep(10)
                log.msg("MISSED URL: "+str(response.url),level=log.WARNING)
                pass
            html_txt = response.body.decode("utf-8","ignore")
            url = response.url
            hxs = Selector(text=html_txt)
            items = hxs.xpath('//div[@class="thumbheader"]/a/@href')
            if items:
                for item in items:
                    book_url = item.extract()
                    log.msg('Request for book: '+ book_url+' is sent out',level=log.INFO)
                    yield Request(url=book_url,callback=self.parse_book)
        except Exception,e:
            log.msg(str(e),level=log.WARNING)
            raise

    def parse_book(self, response):
        html_txt = response.body.decode("utf-8","ignore")
        hxs = Selector(text=html_txt)
        book = Book()
        try:
            if response.status == 403:
                time.sleep(60*5)
                log.msg("FAILURE 403 RESPONSE: "+str(response.url),level=log.ERROR);
                pass
            book['douban_url'] = response.url
            img_container = hxs.xpath('//detailimgcontainer')
            thumbimg = img_container.xpath('.//img[@id="largeImage"]/@src')
            if thumbimg:
                book['img'] = thumbimg.extract()
            info_node = hxs.xpath('.//td[@class="infoTabContent"]')
            if not info_node:
                log.msg("FAILURE NO INFO NODE: "+str(response.url),level=log.ERROR);
                pass

            title_node = info_node.xpath('//dt[contains(text(),"Title")]/../dd[1]/cite/text()')
            if title_node:
                book['title'] = title_node.extract()[0]
            author_node = info_node.xpath('//dt[contains(text(),"By")]/../dd[1]/text()')
            if author_node:
                book['authors'] = author_node.extract()[0]
            publisher_node = info_node.xpath('//dt[contains(text(),"Publisher")]/../dd[1]/text()')
            if publisher_node:
                book['publisher'] = publisher_node.extract()[0]
            page_num_node = info_node.xpath('//dt[contains(text(),"Pages")]/../dd[1]/text()')
            if page_num_node:
                book['page_num'] = page_num_node.extract()[0]
            isbn_node = info_node.xpath('//dt[contains(text(),"ISBN")]/../dd[1]/text()')
            if isbn_node:
                book['isbn'] = isbn_node.extract()[0]
            yield book
        except Exception,e:
            print 'Exception Happened'
            print e
            raise

    def extract_info(self, line):
        if not line:
            return "",""
        line = string.strip(line)
        if not line:
            return "",""

        pos = string.index(line,':')
        if not pos or pos<0:
            return "",""
        field = line[:pos]
        #print "Field: "+field
        value = line[pos+2:]
        #print "Value: "+value
        return field,value

