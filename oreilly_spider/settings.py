# -*- coding: utf-8 -*-

# Scrapy settings for oreilly_spider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'orielly_spider'

SPIDER_MODULES = ['oreilly_spider.spiders']
NEWSPIDER_MODULE = 'oreilly_spider.spiders'
ITEM_PIPELINES = ['oreilly_spider.pipelines.JsonWithEncodingPipeline']
DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
        'oreilly_spider.rotate_useragent.RotateUserAgentMiddleware' :400
    }
DOWNLOAD_DELAY = 2
COOKIES_ENABLED = False
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'oreilly_spider (+http://www.yourdomain.com)'
