import scrapy


class BusinessSpider(scrapy.Spider):
    name = 'business'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    def parse(self, response):
        pass
