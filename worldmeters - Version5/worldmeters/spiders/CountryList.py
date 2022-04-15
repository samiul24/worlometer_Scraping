import scrapy
from ..items import WorldmetersItem
from scrapy.loader import ItemLoader
import logging


class CountrylistSpider(scrapy.Spider):
    name = 'CountryList'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        title = response.xpath("//h1/text()").get()
        countries_data = response.xpath("//tbody/tr")
        #print(countries_data)
        #print(type(countries)) #--> <class 'scrapy.selector.unified.SelectorList'>

        for country_data in countries_data:
            sl_no = country_data.xpath(".//td[1]/text()").get()
            #print(sl_no)
            country = country_data.xpath(".//td[2]/a/text()").get()
            #print(country)
            link = country_data.xpath(".//td[2]/a/@href").get()
            full_link = f"https://www.worldometers.info{link}"
            #print(full_link)

            #yield item.load_item()
            yield response.follow(url=link, callback=self.country_details_by_year, meta={'sl_no':sl_no, 'country':country, 'link':full_link})
        
    def country_details_by_year(self, response):
        item = ItemLoader(item=WorldmetersItem())
        sl_no = response.request.meta['sl_no']
        item.add_value('sl_no', sl_no)

        country = response.request.meta['country']
        item.add_value('country', country)

        link = response.request.meta['link']
        item.add_value('link', link)

        #country_details = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
        country_details = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])")
        for country_table in country_details:
            for country_detail in country_table.xpath(".//tbody/tr"):
                year = country_detail.xpath(".//td[1]/text()").get()
                item.add_value('year', year)

                population = country_detail.xpath(".//td[2]/strong/text()").get()
                item.add_value('population', population)

                yearly_percent_change=country_detail.xpath(".//td[3]/text()").get()
                item.add_value('yearly_percent_change', yearly_percent_change)

                yearly_change=country_detail.xpath(".//td[4]/text()").get()
                item.add_value('yearly_change', yearly_change)

                migrants=country_detail.xpath(".//td[5]/text()").get()
                item.add_value('migrants', migrants)

                median_age=country_detail.xpath(".//td[6]/text()").get()
                item.add_value('median_age', median_age)

                fertility_rate=country_detail.xpath(".//td[7]/text()").get()
                item.add_value('fertility_rate', fertility_rate)

                density=country_detail.xpath(".//td[8]/text()").get()
                item.add_value('density', density)

                urban_percent_pop=country_detail.xpath(".//td[9]/text()").get()
                item.add_value('urban_percent_pop', urban_percent_pop)

                urban_population=country_detail.xpath(".//td[10]/text()").get()
                item.add_value('urban_population', urban_population)

                country_share_of_world_pop=country_detail.xpath(".//td[11]/text()").get()
                item.add_value('country_share_of_world_pop', country_share_of_world_pop)

                global_rank=country_detail.xpath(".//td[12]/text()").get()
                item.add_value('global_rank', global_rank)

                yield item.load_item()

                """yield {
                    'sl_no': sl_no,
                    'country': country,
                    'link': link,
                    'year': year,
                    'population': population,
                }"""


        