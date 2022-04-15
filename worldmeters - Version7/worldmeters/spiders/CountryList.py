import scrapy
from ..items import WorldmetersItem, cleanhtml
from scrapy.loader import ItemLoader
import logging
import time
import sqlite3


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
        sl_no = response.request.meta['sl_no']
        link1 = response.request.meta['link']
        country = response.request.meta['country']
        #item = ItemLoader(item=WorldmetersItem())

        #country_details = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
        country_details = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])")
        table_headers = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])/thead/tr[1]")
        table_headers_list =[]
        for table_header in table_headers.xpath(".//th"):
            table_column = cleanhtml(str(table_header))
            table_headers_list.append(table_column)
            #print(table_column)
        #table_headers_list = list(set(table_headers_list)) # it's used for remove duplicate but does not provide previous secquence
        list_len = int((len(table_headers_list)/2))
        #print(list_len)
        final_table_headers_list = []
        final_table_headers_list = table_headers_list[0:list_len]
        #print(final_table_headers_list)
         

        for country_detail in country_details.xpath(".//tbody/tr"):
            """try:
                final_table_headers_list.remove('countrys_share_of_world_pop')
                final_table_headers_list.remove('world_population')
                final_table_headers_list.remove('global_rank')
            except:
                pass"""

            item = ItemLoader(item=WorldmetersItem())
            default_data = 'N/A'
            sql_cmd = 'INSERT OR IGNORE INTO CountryList(sl_no, country, link, '
            try:
                year = country_detail.xpath(".//td[1]/text()").get()
                #item.add_value(final_table_headers_list[0], str(year))
                sql_cmd = sql_cmd + final_table_headers_list[0] + ' , '
            except:
                year = default_data
                #item.add_value(final_table_headers_list[0], default_data)
                sql_cmd = sql_cmd + final_table_headers_list[0] + ' , '

            try:
                population = country_detail.xpath(".//td[2]/strong/text()").get()
                #item.add_value(final_table_headers_list[1], str(population))
                sql_cmd = sql_cmd + final_table_headers_list[1] + ' , '
            except:
                population = default_data
                #item.add_value(final_table_headers_list[1], default_data)
                sql_cmd = sql_cmd + final_table_headers_list[1] + ' , '

            try:
                yearly_percent_change=country_detail.xpath(".//td[3]/text()").get()
                #item.add_value(final_table_headers_list[2], str(yearly_percent_change))
                sql_cmd = sql_cmd + final_table_headers_list[2] + ' , '
            except:
                yearly_percent_change = default_data
                #item.add_value(final_table_headers_list[2], default_data)
                sql_cmd = sql_cmd + final_table_headers_list[2] + ' , '

            try:
                yearly_change=country_detail.xpath(".//td[4]/text()").get()
                #item.add_value(final_table_headers_list[3], str(yearly_change))
                sql_cmd = sql_cmd + final_table_headers_list[3] + ' , '
            except:
                yearly_change = default_data
                #item.add_value(final_table_headers_list[3], default_data)
                sql_cmd = sql_cmd + final_table_headers_list[3] + ' , '

            try:
                migrants_net=country_detail.xpath(".//td[5]/text()").get()
                #item.add_value(final_table_headers_list[4], str(migrants_net))
                sql_cmd = sql_cmd + final_table_headers_list[4] + ' , '
                """if country == 'Tuvalu':
                    print(country)
                    print(final_table_headers_list[4])
                    print(migrants_net)
                    time.sleep(10)"""

            except:
                migrants_net = default_data
                #item.add_value(final_table_headers_list[4], default_data)
                sql_cmd = sql_cmd + final_table_headers_list[4] + ' , '

            try:
                median_age=country_detail.xpath(".//td[6]/text()").get()
                #item.add_value(final_table_headers_list[5], str(median_age))
                sql_cmd = sql_cmd + final_table_headers_list[5] + ' , '
            except:
                median_age = default_data
                #item.add_value(final_table_headers_list[5], default_data)
                sql_cmd = sql_cmd + final_table_headers_list[5] + ' , '

            try:
                fertility_rate=country_detail.xpath(".//td[7]/text()").get()
                #item.add_value(final_table_headers_list[6], str(fertility_rate))
                sql_cmd = sql_cmd + final_table_headers_list[6] + ' , '
            except:
                fertility_rate = default_data
                #item.add_value(final_table_headers_list[6], default_data)
                sql_cmd = sql_cmd + final_table_headers_list[6] + ' , '

            try:
                density_p_km_percent=country_detail.xpath(".//td[8]/text()").get()
                #item.add_value(final_table_headers_list[7], str(density_p_km_percent))
                sql_cmd = sql_cmd + final_table_headers_list[7] + ' , '
            except:
                density_p_km_percent = default_data
                #item.add_value(final_table_headers_list[7], default_data)
                sql_cmd = sql_cmd + final_table_headers_list[7] + ' , '

            try:
                urban_pop_percent=country_detail.xpath(".//td[9]/text()").get()
                #item.add_value(final_table_headers_list[8], str(urban_pop_percent))
                sql_cmd = sql_cmd + final_table_headers_list[8] + ' , '
            except:
                urban_pop_percent = default_data
                #item.add_value(final_table_headers_list[8], default_data)
                sql_cmd = sql_cmd + final_table_headers_list[8] + ' , '

            try:
                urban_population=country_detail.xpath(".//td[10]/text()").get()
                #item.add_value(final_table_headers_list[9], str(urban_population))
                sql_cmd = sql_cmd + final_table_headers_list[9] + ' , '
            except:
                urban_population = default_data
                #item.add_value(final_table_headers_list[9], default_data)
                sql_cmd = sql_cmd + final_table_headers_list[9] + ' , '

            try:
                countrys_share_of_world_pop=country_detail.xpath(".//td[11]/text()").get()
                #item.add_value(final_table_headers_list[10], str(countrys_share_of_world_pop))
                sql_cmd = sql_cmd + final_table_headers_list[10] + ' , '
            except:
                countrys_share_of_world_pop = default_data
                #item.add_value(final_table_headers_list[10], default_data)
                final_table_headers_list.append('countrys_share_of_world_pop')
                sql_cmd = sql_cmd + final_table_headers_list[10] + ' , '

            try:
                world_population=country_detail.xpath(".//td[12]/text()").get()
                #item.add_value(final_table_headers_list[11], str(world_population))
                sql_cmd = sql_cmd + final_table_headers_list[11] + ' , '
            except:
                world_population = default_data
                #item.add_value(final_table_headers_list[11], default_data)
                final_table_headers_list.append('world_population')
                sql_cmd = sql_cmd + final_table_headers_list[11] + ' , '

            try:
                global_rank=str(country_detail.xpath(".//td[13]/text()").get())
                #item.add_value(final_table_headers_list[12], str(global_rank))
                sql_cmd = sql_cmd +  final_table_headers_list[12] + ' ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '
            except:
                global_rank = default_data
                #item.add_value(final_table_headers_list[12], default_data)
                final_table_headers_list.append('global_rank')
                sql_cmd = sql_cmd +  final_table_headers_list[12] + ' ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '

            item.add_value('sl_no', str(sl_no))
            item.add_value('link', str(link1))
            item.add_value('country', str(country))

            if country != None:
                    print(country)
                    print(final_table_headers_list[4])
                    print(sql_cmd)
                    print(year)
                    print(population)
                    print(yearly_percent_change)
                    print(yearly_change)
                    print(migrants_net)
                    print(median_age)
                    print(fertility_rate)
                    print(density_p_km_percent)
                    print(urban_pop_percent)
                    print(urban_population)
                    print(countrys_share_of_world_pop)
                    print(world_population)
                    print(global_rank)
                    #time.sleep(10)

            self.conn = sqlite3.connect('ScrapyDB.db')
            self.cur = self.conn.cursor()
            self.cur.execute(sql_cmd,
            ( sl_no, country, link1, year, population, yearly_percent_change,
             yearly_change, migrants_net, median_age, fertility_rate, density_p_km_percent, urban_pop_percent, 
            urban_population, countrys_share_of_world_pop, world_population, global_rank ))
            self.conn.commit()

            #yield item.load_item()
                
            """yield{
                'sl_no': sl_no,
                'link': link1,
                'country': country,
                'year': year,
                'population': population,
                'yearly_percent_change': yearly_percent_change,
                'yearly_change': yearly_change,
                'migrants_net': a,
                'median_age': median_age,
                'fertility_rate': fertility_rate,
                'density_p_km_percent': density_p_km_percent,
                'urban_pop_percent': urban_pop_percent,
                'urban_population': urban_population,
                'countrys_share_of_world_pop': countrys_share_of_world_pop,
                'world_population': world_population,
                'global_rank': global_rank,
                'final_table_headers_list' : final_table_headers_list,

            }"""


        
            


        