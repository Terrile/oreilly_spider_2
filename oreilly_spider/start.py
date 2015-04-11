# -*- coding: utf-8 -*-
from scrapy import cmdline
import re
import string
__author__ = 'Min'

if __name__ == "__main__":
    cmdline.execute("scrapy crawl oreillyspider --logfile=log.txt".split())