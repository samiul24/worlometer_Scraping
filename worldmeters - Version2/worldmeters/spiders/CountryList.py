import scrapy
from ..items import WorldmetersItem
from scrapy.loader import ItemLoader


class CountrylistSpider(scrapy.Spider):
    name = 'CountryList'
    allowed_domains = ['www.worldometers.info/']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        title = response.xpath("//h1/text()").get()
        countries = response.xpath("//td/a")
        #print(countries)
        #print(type(countries)) #--> <class 'scrapy.selector.unified.SelectorList'>
        for country in countries:
            item = ItemLoader(item=WorldmetersItem())
            #print(country)

            name = country.xpath(".//text()").get()
            #print(name)
            item.add_value('name', name)

            link = country.xpath(".//@href").get()
            #print(link)
            item.add_value('link', str(link))

            #print(item.add_value)
            yield item.load_item()