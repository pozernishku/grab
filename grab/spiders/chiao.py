# -*- coding: utf-8 -*-
import scrapy
import html
import re
from urllib.parse import urlparse
from grab.items import GrabItem

class ChiaoSpider(scrapy.Spider):
    name = 'chiao'
    allowed_domains = ['www.ciao.nl']
    start_urls = ['https://www.ciao.nl/search?query=a&page=1']
    regex_href = re.compile(r"\b(?:https?://|www\.)+\S{3,}", re.MULTILINE | re.IGNORECASE)

    def parse(self, response):
        hrefs = response.xpath('//div[@class="content-offers"]/a/@href').getall()
        for href in hrefs:
            yield response.follow(html.unescape(href), self.parse_domain, dont_filter=True)

    def parse_domain(self, response):
        r_url = html.unescape(response.url)
        yield response.follow(r_url, self.parse_pure_domain, meta={'r_url': r_url}, dont_filter=True)

    def parse_pure_domain(self, response):
        third_script = response.xpath('//script[3]').get(default='')
        href = ''.join(self.regex_href.findall(third_script)).strip(', "')

        yield response.follow(html.unescape(href), self.parse_pure_domain_redirected, meta=response.meta, dont_filter=True)


    def parse_pure_domain_redirected(self, response):
        domain = urlparse(response.url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=domain)
        # domain = urlparse(href)
        # domain = '{uri.scheme}://{uri.netloc}/'.format(uri=domain)
        yield GrabItem(domain = domain,
                       r_url = response.meta.get('r_url'))