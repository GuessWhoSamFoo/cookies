# -*- coding: utf-8 -*-

import logging
import scrapy
from scrapy import Item, Field
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class Docs404Item(Item):
    referer = Field()
    status = Field()
    url = Field()

class Docs404Spider(CrawlSpider):
    def __init__(self, *args, **kwargs):
        logger = logging.getLogger('scrapy.core.engine')
        logger.setLevel(logging.WARNING)
        super().__init__(*args, **kwargs)

#    DOWNLOAD_DELAY=0.1
    name = 'docs404'
    allowed_domains = ['localhost' ]
    start_urls = ['http://localhost:1313/docs']
    handle_httpstatus_list = [404]

    rules = (
        Rule(LinkExtractor(allow=r'/docs/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = Docs404Item()
        
        if response.status == 404:
            item['referer'] = response.request.headers.get('Referer')
            item['status'] = response.status
            item['url'] = response.url
        
            return item
