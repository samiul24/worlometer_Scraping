# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags


class WorldmetersItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    population = scrapy.Field(output_processor=TakeFirst())
    yearly_change = scrapy.Field(output_processor=TakeFirst())
    net_change = scrapy.Field(output_processor=TakeFirst())
    lead_area = scrapy.Field(output_processor=TakeFirst())
    migrants = scrapy.Field(output_processor=TakeFirst())
    fert_rate = scrapy.Field(output_processor=TakeFirst())
    med_age = scrapy.Field(output_processor=TakeFirst())
    urban_pop = scrapy.Field(output_processor=TakeFirst())
    world_share = scrapy.Field(output_processor=TakeFirst())
    pass
