import loguru
import json
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import sqlalchemy
import sqlalchemy.ext.automap

from ..database.connection import session, metadata, automap

class BusinessSpider(scrapy.Spider):
    name = 'business'
    __sourcetable__ = 'crawler_source'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
 
    def get_source_path(self, sourceId):
        sqlalchemy.Table(self.__sourcetable__, metadata, autoload=True)
        Source = automap.classes[self.__sourcetable__]
        self.source = session.query(Source).filter(
            Source.id == int(sourceId)
        ).one()
        self.schema = json.loads(self.source.crawler_schema)
        #loguru.logger.info(f'{self.source.topics}-{self.source.name}')
        #loguru.logger.info(f'{schema["page_title"]}')
        self.rules = {
            Rule(LinkExtractor(restrict_xpaths=self.schema["page_title"]), callback='parse_item', follow=True, process_request='set_user_agent'),
            Rule(LinkExtractor(restrict_xpaths=self.schema["next_page"]), process_request='set_user_agent')
        }

    def start_requests(self):
        sourceId = getattr(self, 'id', None)
        if sourceId is not None:
            self.get_source_path(sourceId)
            yield scrapy.Request(url=self.source.crawler_url, meta={'source_id':self.source.id, 'topics':self.source.topics}, callback=self.parse)
        else:
            print('Please add parameter at command, e.g. scrapy crawl business -a id=5')

    def parse(self, response):
        yield{
            'source_id':response.meta['source_id'],
            'topics':response.meta['topics'],
            'article_url':response.url,
            'title':response.xpath(self.schema["title"]).get(),
            'source_content':(response.xpath(self.schema["source_content"]).get()).replace("\n","")
        }


        
