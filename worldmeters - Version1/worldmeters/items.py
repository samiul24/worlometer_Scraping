# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags


class WorldmetersItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass
