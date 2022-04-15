import scrapy
from ..items import WorldmetersItem
from scrapy.loader import ItemLoader


class CountrylistSpider(scrapy.Spider):
    name = 'CountryList'
    allowed_domains = ['www.worldometers.info/']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        title = response.xpath("//h1/text()").get()
        countries = response.xpath("//td/a/text()").getall()
        #print(countries)
        #print(type(countries)) --> List
        for country in countries:
            print(country)
            #print(type(country)) --> Str
            item = ItemLoader(item=WorldmetersItem())
            #print(item)
            item.add_value('name', country)
            #print(item.add_value)
            yield item.load_item()