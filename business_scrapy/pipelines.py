# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from database.connection import session
from database.models import ListData, ArticleData


class BusinessScrapyPipeline:
    def process_item(self, item, spider):

        return item

    def close_spider(self, spider):
        try:
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()
