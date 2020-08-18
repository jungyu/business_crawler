'''
TODO:
資料表 crawler_source 欄位定義及範例：
  crawler_url = http://books.toscrape.com, http://... 使用逗號, 分隔
  crawler_schema = {"allowed_domain": ["books.toscrape.com"], "allow": "catalogue/", "xpath_exists": "//div[@id=\"product_gallery\"]", "xpath_title": "//div/h1/text()", "xpath_image":"//div[@class=\"item active\"]/img/@src", "xpath_description": "//div[@id=\"product_description\"]/following-sibling::p/text()"}
'''
import sys
import re
import loguru
import json
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import sqlalchemy
import sqlalchemy.ext.automap

from ..database.connection import session, metadata, automap
from ..items import BusinessScrapyItem

class Param():
    def __init__(self):
        if sys.argv[3].find("id=") > -1:
            self.source_id = sys.argv[3].replace('id=', '')
            try:
                self.source_id = int(self.source_id)
            except ValueError:
                print('Parameter id must be number.')
                self.source_id = 1
        else:
            print('Please add parameter at command, e.g. scrapy crawl business -a id=6')
            self.source_id = 1

    def get_source_id(self):
        return self.source_id
   
class BusinessSpider(CrawlSpider):
    name = 'business'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    __sourcetable__ = 'crawler_source'

    param = Param()
    source_id = param.get_source_id()
    loguru.logger.info('source_id:' + str(source_id))

    #從資料庫讀取 source
    sqlalchemy.Table(__sourcetable__, metadata, autoload=True)
    Source = automap.classes[__sourcetable__]
    source = session.query(Source).filter(
        Source.id == int(source_id)
    ).one()

    try:
        schema = json.loads(source.crawler_schema)
    except:
        loguru.logger.error('Schema 之 JSON 結構錯誤!! 請檢查 crawler_source 資料表中 schema 欄位內的格式')

    loguru.logger.info(schema)
    
    allowed_domains = schema['allowed_domain'] #['books.toscrape.com']
    start_urls = re.split(",", source.crawler_url) #['http://books.toscrape.com/']
    base_url = source.source_domain #'http://books.toscrape.com/'
    loguru.logger.info(start_urls)

    #allow='catalogue/'
    '''rules = [Rule(LinkExtractor(allow=schema['allow']),
                  callback='parse_filter_book', follow=True)]'''

    '''rules = [Rule(LinkExtractor(allow=schema['allow'], restrict_xpaths="//div[@class='container article-list__container']"), callback='parse_filter_book', follow=True)]'''
    rules = [Rule(LinkExtractor(allow=schema['allow'], restrict_xpaths=schema['extractor_link']),callback='parse_filter_book', follow=True),
             Rule(LinkExtractor(restrict_xpaths=schema['extractor_next']))]

    def parse_filter_book(self, response):
        exists = response.xpath(self.schema['xpath_exists']).extract_first()
        if exists:

            business = BusinessScrapyItem()

            title = response.xpath(self.schema['xpath_title']).extract_first()

            relative_image = response.xpath(self.schema['xpath_image']).extract_first()
            final_image = self.base_url + relative_image.replace('../..', '')

            description = response.xpath(self.schema['xpath_description']).extract_first()

            business['source_id'] = self.source.id
            business['topics'] = self.source.topics
            business['article_url'] = response.url

            business['title'] = title
            business['final_image'] = final_image
            business['description'] = description

            yield business

            '''
            XPath 範例
            price = response.xpath(
                '//div[contains(@class, "product_main")]/p[@class="price_color"]/text()').extract_first()
            stock = response.xpath(
                '//div[contains(@class, "product_main")]/p[contains(@class, "instock")]/text()').extract()[1].strip()
            stars = response.xpath(
                '//div/p[contains(@class, "star-rating")]/@class').extract_first().replace('star-rating ', '')
            description = response.xpath(
                '//div[@id="product_description"]/following-sibling::p/text()').extract_first()
            upc = response.xpath(
                '//table[@class="table table-striped"]/tr[1]/td/text()').extract_first()
            price_excl_tax = response.xpath(
                '//table[@class="table table-striped"]/tr[3]/td/text()').extract_first()
            price_inc_tax = response.xpath(
                '//table[@class="table table-striped"]/tr[4]/td/text()').extract_first()
            tax = response.xpath(
                '//table[@class="table table-striped"]/tr[5]/td/text()').extract_first()
            
            
            book['price'] = price
            book['stock'] = stock
            book['stars'] = stars
            book['upc'] = upc
            book['price_excl_tax'] = price_excl_tax
            book['price_inc_tax'] = price_inc_tax
            book['tax'] = tax
            '''
            

        else:
            print(response.url)


        
