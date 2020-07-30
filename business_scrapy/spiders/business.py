import scrapy

import sqlalchemy
import sqlalchemy.ext.automap
import sqlalchemy.orm
import sqlalchemy.schema

from ..database.connection import session, metadata, automap


class BusinessSpider(scrapy.Spider):
    name = 'business'

    
    sqlalchemy.Table('crawler_source', metadata, autoload=True)
    Source = automap.classes['crawler_source']

    def start_requests(self):
        sourceId = getattr(self, 'id', None)
        if sourceId is not None:
            
            result = session.query(Source).filter(
                Source.id == sourceId
            ).one()
            print(result)

        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
