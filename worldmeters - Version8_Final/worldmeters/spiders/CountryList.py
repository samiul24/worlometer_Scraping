import scrapy
from ..items import WorldmetersItem, cleanhtml, data_clean
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
            country = cleanhtml(country_data.xpath(".//td[2]/a/text()").get())
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
        table_headers = response.xpath("((//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])/thead/tr[1])[1]")
        table_headers_list =[]
        table_headers_sql_cmd = '"""INSERT OR IGNORE INTO CountryList(sl_no,link,country'
        table_headers_sql_value = ' VALUES'
        for table_header in table_headers.xpath(".//th"):
            table_column = cleanhtml(str(table_header))
            table_headers_list.append(table_column)
            table_headers_sql_cmd = table_headers_sql_cmd + ',' + table_column
            #table_headers_sql_value = table_headers_sql_value + ',?'
        
        table_headers_sql_cmd = table_headers_sql_cmd + ')'
        #table_headers_sql_value = table_headers_sql_value + ')'
        sql_cmd_real = table_headers_sql_cmd + table_headers_sql_value
        #print(sql_cmd_real)

        for country_detail in country_details.xpath(".//tbody/tr"):
            item = ItemLoader(item=WorldmetersItem())
            default_data = 'N/A'
            data_list = []
            sql_value_real = ''

            try:
                A = country_detail.xpath(".//td[1]/text()").get()
                sql_value_real = '('+"'"+sl_no+"'"+','+"'"+str(link1)+"'"+','+"'"+str(country)+"'"+','+data_clean(A)
            except:
                A = default_data

            try:
                B = country_detail.xpath(".//td[2]/strong/text()").get()
                sql_value_real = sql_value_real + ',' + data_clean(B)
            except:
                B = default_data

            try:
                C = country_detail.xpath(".//td[3]/text()").get()
                sql_value_real = sql_value_real + ',' + data_clean(C)
            except:
                C = default_data

            try:
                D = country_detail.xpath(".//td[4]/text()").get()
                sql_value_real = sql_value_real + ',' + data_clean(D)
            except:
                D = default_data

            try:
                E = country_detail.xpath(".//td[5]/text()").get()
                sql_value_real = sql_value_real + ',' + data_clean(E)
                """if country == 'Tuvalu':
                    print(country)
                    print(final_table_headers_list[4])
                    print(migrants_net)
                    time.sleep(10)"""

            except:
                E = default_data

            try:
                F = str(country_detail.xpath(".//td[6]/text()").get())
                sql_value_real = sql_value_real + ',' + data_clean(F)
            except:
                F = default_data

            try:
                G = str(country_detail.xpath(".//td[7]/text()").get())
                sql_value_real = sql_value_real + ',' + data_clean(G)
            except:
                G = default_data

            try:
                H = str(country_detail.xpath(".//td[8]/text()").get())
                sql_value_real = sql_value_real + ',' + data_clean(H)
            except:
                H = default_data

            try:
                I = str(country_detail.xpath(".//td[9]/text()").get())
                if I != 'None':
                    sql_value_real = sql_value_real + ',' + data_clean(I)
            except:
                I = default_data

            try:
                J = str(country_detail.xpath(".//td[10]/text()").get())
                if J != 'None':
                    sql_value_real = sql_value_real + ',' + data_clean(J)
            except:
                J = default_data

            try:
                K = str(country_detail.xpath(".//td[11]/text()").get())
                if K != 'None':
                    sql_value_real = sql_value_real + ',' + data_clean(K)
            except:
                K = default_data

            try:
                L = str(country_detail.xpath(".//td[12]/text()").get())
                if L != 'None':
                    sql_value_real = sql_value_real + ',' + data_clean(L)
            except:
                L = default_data

            try:
                row_existing_check = country_detail.xpath(".//td[13]")
                #print(row_existing_check) 
                M = str(country_detail.xpath(".//td[13]/text()").get())
                if row_existing_check and M != 'None':  
                    sql_value_real = sql_value_real + ',' + data_clean(M)
                elif row_existing_check and M == 'None':
                    sql_value_real = sql_value_real + ',' + data_clean(default_data)
            except:
                M = default_data
            
            sql_value_real = sql_cmd_real + sql_value_real +')"""'
            #print(sql_value_real)

            item.add_value('sl_no', str(sl_no))
            item.add_value('link', str(link1))
            item.add_value('country', str(country))                    

            self.conn = sqlite3.connect('ScrapyDB.db')
            self.cur = self.conn.cursor()
            try:
                self.cur.execute(sql_value_real)
                self.conn.commit()
            except:
                with open('E:\Project Work\Online Content\Scrapy\Projects\worldmeters\InsertCommand.txt', 'a') as f:
                    f.write(sql_value_real)
                    f.write('\n')
                    f.close()
            

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


        
            


        