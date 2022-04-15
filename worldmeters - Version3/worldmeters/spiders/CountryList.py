import scrapy
from ..items import WorldmetersItem
from scrapy.loader import ItemLoader


class CountrylistSpider(scrapy.Spider):
    name = 'CountryList'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        title = response.xpath("//h1/text()").get()
        countries_data = response.xpath("//tbody/tr")
        print(countries_data)
        #print(type(countries)) #--> <class 'scrapy.selector.unified.SelectorList'>
        for country_data in countries_data:
            item = ItemLoader(item=WorldmetersItem())
            #print(country)
            
            sl_no = country_data.xpath(".//td[1]/text()").get()
            print(sl_no)
            item.add_value('sl_no', sl_no)

            country = country_data.xpath(".//td[2]/a/text()").get()
            print(country)
            item.add_value('country', country)

            link = country_data.xpath(".//td[2]/a/@href").get()
            link = f"https://www.worldometers.info{link}"
            print(link)
            item.add_value('link', str(link))

            population = country_data.xpath(".//td[3]/text()").get()
            print(population)
            item.add_value('population', population)

            yearly_change = country_data.xpath(".//td[4]/text()").get()
            print(yearly_change)
            item.add_value('yearly_change', yearly_change)

            net_change = country_data.xpath(".//td[5]/text()").get()
            print(net_change)
            item.add_value('net_change', net_change)

            lead_area = country_data.xpath(".//td[6]/text()").get()
            print(lead_area)
            item.add_value('lead_area', lead_area)

            migrants = country_data.xpath(".//td[7]/text()").get()
            print(migrants)
            item.add_value('migrants', migrants)

            fert_rate = country_data.xpath(".//td[8]/text()").get()
            print(fert_rate)
            item.add_value('fert_rate', fert_rate)

            med_age = country_data.xpath(".//td[9]/text()").get()
            print(med_age)
            item.add_value('med_age', med_age)

            urban_pop = country_data.xpath(".//td[10]/text()").get()
            print(urban_pop)
            item.add_value('urban_pop', urban_pop)

            world_share = country_data.xpath(".//td[11]/text()").get()
            print(world_share)
            item.add_value('world_share', world_share)

            #print(item.add_value)
            yield item.load_item()