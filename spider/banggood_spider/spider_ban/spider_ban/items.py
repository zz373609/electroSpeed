# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
   _id = scrapy.Field()
   url = scrapy.Field()
   images = scrapy.Field()
   title = scrapy.Field()
   rate = scrapy.Field()
   reviews = scrapy.Field()
   price = scrapy.Field()
   color = scrapy.Field()
   size = scrapy.Field()
   sold = scrapy.Field()
   description = scrapy.Field()
   category = scrapy.Field()

