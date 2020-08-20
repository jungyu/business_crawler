import sys
import re
import loguru
import json

import sqlalchemy
import sqlalchemy.ext.automap

from ..database.connection import session, metadata, automap

class Wordpress():

    __articletable__ = 'crawler_article'
    __articlemetatable__ = 'crawler_articlemeta'
    __fieldstable__ = 'crawler_fields'
    __listtable__ = 'crawler_list'

    __wp_posts_table__ = 'wp_posts'
    __wp_postmeta_table__ = 'wp_postmeta'
    __wp_term_relationships_table__ = 'wp_term_relationships'
    __wp_term_taxonomy_table__ = 'wp_term_taxonomy'
    __wp_termmeta__ = 'wp_termmeta'
    __wp_terms__ = 'wp_terms'

    source_id = 0


    def __init__(self, source_id):
        loguru.logger.info('init')
        self.source_id = source_id

        #從資料庫讀取 source
        sqlalchemy.Table(self.__fieldstable__, metadata, autoload=True)
        Fields = automap.classes[self.__fieldstable__]
        fields = session.query(Fields).filter(
            Fields.source_id == int(source_id)
        ).one()

        print(fields.source_fields)
        print(fields.target_fields)

    def main(self):
        loguru.logger.info('main')

    def start_parse(self):
        loguru.logger.info('start_parse')

'''
crawler_fields 資料表

source_fields 欄位內容：
{
   "xpath_author":"//div[@class=\"pc-bigArticle\"]/a/text()",
   "xpath_author_url":"//div[@class=\"pc-bigArticle\"]/a/@href",
   "xpath_title":"//article[@class=\"pc-bigArticle\"]//h1",
   "xpath_abstract":"//meta[@name=\"description\"]/@content",
   "xpath_subtitles":"//section[@class=\"article-content\"]/h3/text()",
   "xpath_content":"//section[@class=\"article-content\"]",
   "xpath_terms":"",
   "xpath_tags":"//ul[@class=\"BreadCrumbs\"]/li/a/text()",
   "xpath_publish_date":"//div[@class=\"article-time\"]/text()",
   "xpath_images":"//section[@class=\"article-content\"]//img/@src",
   "xpath_images_alter":"//section[@class=\"article-content\"]//img/@alt",
   "xpath_images_caption":"//section[@class=\"article-content\"]//img/following-sibling::span[@class=\"article-figcaption\"]",
   "image_url_prefix":"",
   "terms_ignore_indexs":"",
   "tags_ignore_indexs":"1"
}

target_fields 欄位內容：
{
   "wp_posts":{
        "article":{
            "post_date":"xpath_publish_date",
            "post_content":"xpath_content",
            "post_title":"xpath_title",
            "post_excerpt":"xpath_abstract"
        },
        "images":{
            "post_date":"xpath_publish_date",
            "post_title":"xpath_images_alter",
            "post_excerpt":"xpath_images_caption"
        }
    },
   "wp_postmea":{
        "author_name":"xpath_author",
        "author_url": "xpath_author_url",
        "subtitles":"xpath_subtitles"
    },    
   "wp_terms":{
        "tags":{
           "name":"xpath_tags"
        },
        "terms":{
           "name":"xpath_terms"
        }
   }
}
'''
    
