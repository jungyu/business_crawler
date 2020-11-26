# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
    
class BusinessScrapyItem(scrapy.Item):
    source_id = scrapy.Field()
    topics = scrapy.Field()
    article_url = scrapy.Field()

    title = scrapy.Field()
    final_image = scrapy.Field()
    description = scrapy.Field()
    publish_date = scrapy.Field()
    
'''
class BooksItem(scrapy.Item):
    price = scrapy.Field()
    stock = scrapy.Field()
    stars = scrapy.Field()
    description = scrapy.Field()
    upc = scrapy.Field()
    price_excl_tax = scrapy.Field()
    price_inc_tax = scrapy.Field()
    tax = scrapy.Field()
'''