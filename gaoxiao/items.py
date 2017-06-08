# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GaoxiaoItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    province = scrapy.Field()
    college = scrapy.Field()


class CnblogImageItem(scrapy.Item):
    image = scrapy.Field()
    imagePath = scrapy.Field()
    name = scrapy.Field()
