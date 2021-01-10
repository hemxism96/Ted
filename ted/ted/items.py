# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class TedItem(scrapy.Item):
    # define the fields for your item here like:

    url = scrapy.Field()    
    title= scrapy.Field()   
    keywords= scrapy.Field()   
    author= scrapy.Field()   
    description= scrapy.Field()
    uploadDate = scrapy.Field()
    views = scrapy.Field()
    duration = scrapy.Field()
    languages = scrapy.Field()
    thumbnail = scrapy.Field()

class VocalItem(scrapy.Item):

    url = scrapy.Field()
    title = scrapy.Field()
    keywords = scrapy.Field()
    author = scrapy.Field()
    description= scrapy.Field()
    uploadDate = scrapy.Field()
    image = scrapy.Field()