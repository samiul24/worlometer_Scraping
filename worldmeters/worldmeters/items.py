# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags
import re
import time

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  cleantext = cleantext.replace('>', "")
  cleantext = cleantext.replace("'", "")
  cleantext = cleantext.replace("(", "")
  cleantext = cleantext.replace(")", "")
  cleantext = cleantext.replace("%", "percent")
  cleantext = cleantext.replace("/", "_")
  cleantext = cleantext.replace("²", "_percent")
  cleantext = cleantext.replace("'", "")
  
  if (cleantext.find('ank') != -1 or cleantext.find('lobal') != -1):
    cleantext = 'global rank'
  
  if (cleantext.find('hare') != -1):
    cleantext = 'countrys_share_of_world_pop'

  cleantext = cleantext.replace(" ", "_")
  cleantext = cleantext.replace("__", "_")

  return cleantext.lower()

def data_clean(raw_data):
  cleandata = raw_data.replace(" ", "")
  cleandata = cleandata.replace(",", "")

  return "'"+str(cleandata)+"'"


class WorldmetersItem(scrapy.Item):
    # define the fields for your item here like:
    sl_no = scrapy.Field(output_processor=TakeFirst())
    country = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    year = scrapy.Field(output_processor=TakeFirst())
    population = scrapy.Field(output_processor=TakeFirst())
    yearly_percent_change = scrapy.Field(output_processor=TakeFirst())
    yearly_change = scrapy.Field(output_processor=TakeFirst())
    migrants_net = scrapy.Field(output_processor=TakeFirst())
    median_age = scrapy.Field(output_processor=TakeFirst())
    fertility_rate = scrapy.Field(output_processor=TakeFirst())
    density_p_km_percent = scrapy.Field(output_processor=TakeFirst())
    urban_pop_percent = scrapy.Field(output_processor=TakeFirst())
    urban_population = scrapy.Field(output_processor=TakeFirst())
    countrys_share_of_world_pop = scrapy.Field(output_processor=TakeFirst())
    world_population = scrapy.Field(output_processor=TakeFirst())
    global_rank = scrapy.Field(output_processor=TakeFirst())
    #pass