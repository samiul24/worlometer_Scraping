# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags


class WorldmetersItem(scrapy.Item):
    # define the fields for your item here like:
    sl_no = scrapy.Field(output_processor=TakeFirst())
    country = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    year = scrapy.Field(output_processor=TakeFirst())
    population = scrapy.Field(output_processor=TakeFirst())
    yearly_percent_change = scrapy.Field(output_processor=TakeFirst())
    yearly_change = scrapy.Field(output_processor=TakeFirst())
    migrants = scrapy.Field(output_processor=TakeFirst())
    median_age = scrapy.Field(output_processor=TakeFirst())
    fertility_rate = scrapy.Field(output_processor=TakeFirst())
    density = scrapy.Field(output_processor=TakeFirst())
    urban_percent_pop = scrapy.Field(output_processor=TakeFirst())
    urban_population = scrapy.Field(output_processor=TakeFirst())
    country_share_of_world_pop = scrapy.Field(output_processor=TakeFirst())
    global_rank = scrapy.Field(output_processor=TakeFirst())
    
