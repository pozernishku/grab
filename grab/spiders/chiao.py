# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlparse
from grab.items import GrabItem

class ChiaoSpider(scrapy.Spider):
    name = 'chiao'
    allowed_domains = ['www.ciao.nl']
    start_urls = ['https://www.ciao.nl/search?query=a&page=1']

    def parse(self, response):
        hrefs = response.xpath('//div[@class="content-offers"]/a/@href').getall()
        for href in hrefs:
            yield response.follow(href, self.parse_domain, dont_filter=True)

    def parse_domain(self, response):
        domain = urlparse(response.url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=domain)
        self.log('>> ' + domain)

        yield GrabItem(domain=domain)