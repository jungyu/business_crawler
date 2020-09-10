import sys
import re
import loguru
import urllib
import json
import time
from datetime import datetime

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
    __wp_termmeta_table__ = 'wp_termmeta'
    __wp_terms_table__ = 'wp_terms'

    source_id = 0
    topics = None
    fields = None

    def __init__(self, source_id, topics):
        loguru.logger.info('init')
        self.source_id = source_id
        self.topics = topics

    def main(self):
        loguru.logger.info('main')
        self.get_fields()
        articles = self.get_articles()
        posts = self.compose_articles(articles)
        self.to_wordpress(posts)

    def get_fields(self):
        loguru.logger.info('get_fields')
        #從資料庫讀取 source
        sqlalchemy.Table(self.__fieldstable__, metadata, autoload=True)
        Fields = automap.classes[self.__fieldstable__]
        fields = session.query(Fields).filter(
            Fields.source_id == int(self.source_id)
        ).order_by(
            Fields.id.desc()
        ).first()

        self.fields = fields
        print(self.fields.source_fields)
        print(self.fields.target_fields)

    def get_articles(self):
        loguru.logger.info('get_articles')
        #TODO:從資料庫合併查詢 list ,article, articlemeta 及 article_media
        sqlalchemy.Table(self.__listtable__, metadata, autoload=True)
        Listtable = automap.classes[self.__listtable__]

        sqlalchemy.Table(self.__articletable__, metadata, autoload=True)
        Articletable = automap.classes[self.__articletable__]

        articles = session.query(
            Listtable, Articletable
        ).filter(
            Listtable.source_id == int(self.source_id),
            Listtable.id == Articletable.list_id
        ).with_entities(
            Listtable.id,
            Listtable.topic,
            Listtable.article_url,
            Articletable.title,
            Articletable.source_content
        ).all()

        return articles

    #組合 fields, articles ...等
    def compose_articles(self, articles):
        loguru.logger.info('compose_articles: ' + self.topics)
        return articles

    def to_wordpress(self, posts):
        loguru.logger.info('Write article to wordpress.')
        termIds = self.find_or_insert_term(self.topics)
        self.insert_or_update_posts(termIds, posts)

    def insert_or_update_posts(self, termIds, posts):
        loguru.logger.info('insert_or_update_posts')

        current_time = datetime.now().timetuple()

        sqlalchemy.Table(self.__wp_posts_table__, metadata, autoload=True)
        Poststable = automap.classes[self.__wp_posts_table__] 

        for post in posts:
            slug = urllib.parse.quote(post.title, encoding="utf8")
            slug = slug[:220] + '_id_' + str(self.source_id)
            loguru.logger.info(slug)
            '''
            poststable = Poststable()
            poststable.post_author = '1'
            poststable.post_date = current_time
            poststable.post_date_gmt = current_time
            poststable.post_content = post.source_content
            poststable.post_title = post.title
            poststable.post_excerpt = ''
            poststable.post_status = 'publish'
            poststable.comment_status = 'closed'
            poststable.ping_status = 'closed'
            poststable.post_password = ''
            poststable.post_name = slug
            poststable.to_ping = ''
            poststable.pinged = ''
            poststable.post_modified =  current_time
            poststable.post_modified_gmt = current_time
            poststable.post_content_filtered = ''
            poststable.post_parent = '0'
            poststable.guid = ''
            poststable.menu_order = 0
            poststable.post_type = 'post'
            poststable.post_mime_type = ''
            poststable.comment_count = '0'
            session.add(poststable)
            session.flush()
            '''
            #self.process_postmeta(poststable.ID, post)
            #self.process_categories(poststable.ID, termIds)

        try:
            session.commit()
        except Exception as e:
            loguru.logger.error('新增資料失敗')
            loguru.logger.error(e)
            session.rollback()
        finally:
            session.close()


    def process_postmeta(self, ID, post):
        loguru.logger.info('process_postmeta')
        sqlalchemy.Table(self.__wp_postmeta_table__, metadata, autoload=True)
        Postmetatable = automap.classes[self.__wp_postmeta_table__]

        #source_url
        postmetatable = Postmetatable()
        postmetatable.post_id = ID
        postmetatable.meta_key = 'source_url'
        postmetatable.meta_value = post.article_url
        session.add(postmetatable)
        session.flush()
        

    def process_categories(self, ID, termIds):
        loguru.logger.info('process_categories')
        self.find_or_insert_relation(ID, termIds)
        #TOFIX: count to taxonomy


    def find_or_insert_term(self, topics):
        loguru.logger.info('find_or_insert_term')
        slug = urllib.parse.quote(topics, encoding="utf8")
        loguru.logger.info(slug)

        sqlalchemy.Table(self.__wp_terms_table__, metadata, autoload=True)
        Termstable = automap.classes[self.__wp_terms_table__]
        termstable = Termstable()
        termstable.name = topics
        termstable.slug = slug
        termstable.term_group = '0'
        session.add(termstable)
        session.flush()

        term_id = termstable.term_id

        sqlalchemy.Table(self.__wp_term_taxonomy_table__, metadata, autoload=True)
        Taxonomytable = automap.classes[self.__wp_term_taxonomy_table__]
        taxonomytable = Taxonomytable()
        taxonomytable.term_id = term_id
        taxonomytable.taxonomy = 'category'
        taxonomytable.description = ''
        taxonomytable.parent = '0'
        session.add(taxonomytable)
        session.flush()

        try:
            session.commit()
        except Exception as e:
            loguru.logger.error('新增分類失敗')
            loguru.logger.error(e)
            session.rollback()
            return 0
        finally:
            session.close()
            return term_id

    def find_or_insert_relation(self, ID, termIds):
        loguru.logger.info('find_or_insert_relation')
        sqlalchemy.Table(self.__wp_term_relationships_table__, metadata, autoload=True)
        Relationtable = automap.classes[self.__wp_term_relationships_table__]
        relationtable = Relationtable()
        relationtable.object_id = ID
        relationtable.term_taxonomy_id = termIds
        relationtable.term_order = '0'
        session.add(relationtable)
        session.flush()


        

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
    
