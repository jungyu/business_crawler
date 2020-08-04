# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import loguru
import json

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from itemadapter import ItemAdapter

import sqlalchemy
import sqlalchemy.ext.automap
from ..database.connection import session, metadata, automap


class BusinessScrapyPipeline:
    __articletable__ = 'crawler_article'
    __articlemetatable__ = 'crawler_articlemeta'
    __fieldstable__ = 'crawler_fields'
    __listtable__ = 'crawler_list'
    __mediatable__ = 'crawler_media'
    
    def process_item(self, item, spider):
        global source
        created = int(time.mktime(datetime.now().timetuple()))

        sqlalchemy.Table(self.__listtable__, metadata, autoload=True)
        sqlalchemy.Table(self.__articletable__, metadata, autoload=True)

        Article = automap.classes[self.__articletable__]
        Alist = automap.classes[self.__listtable__]
        loguru.logger.info(source)
        '''
        Q1.如何跨類傳遞參數
        Q2.如何還沒 commit 前，取得 list id
        alist = Alist()
        alist.source_id = source.id
        alist.topic = source.topics #TOFIX
        alist.article_title = title
        alist.article_url = perma_link
        alist.created = created
        session.add(alist)

        article = Article()
        article.title = item['title'].encode('utf-8')
        article.source_title = item['source_content'].encode('utf-8')
        session.add(article)
        '''

        
        return item

    def close_spider(self, spider):
        try:
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()
