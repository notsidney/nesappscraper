# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class doc_item(scrapy.Item):
    doc_name = scrapy.Field()
    doc_link = scrapy.Field()

class exam_pack_item(scrapy.Item):
    course = scrapy.Field()
    year = scrapy.Field()
    link = scrapy.Field()
    docs = scrapy.Field()

class course_item(scrapy.Item):
    course_name = scrapy.Field()
    packs = scrapy.Field()
