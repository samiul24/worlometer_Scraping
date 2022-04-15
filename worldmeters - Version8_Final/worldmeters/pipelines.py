# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
import time

class WorldmetersPipeline:
    def __init__(self):
        self.conn = sqlite3.connect('ScrapyDB.db')
        self.cur = self.conn.cursor()
        self.create_table()


    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS CountryList
        (sl_no Text, country Text, link Text, year text, population Text, yearly_percent_change text, 
        yearly_change Text, migrants_net Text, median_age Text, fertility_rate Text, density_p_km_percent Text, 
        urban_pop_percent Text, urban_population Text, countrys_share_of_world_pop Text, world_population Text, global_rank text)""")

    def process_item(self, item, spider):
        print(item['year'])
        print(item['migrants_net'])
        print(item['density_p_km_percent'])
        if item['country']=='Tuvalu':
            time.sleep(100)

        self.cur.execute("""INSERT OR IGNORE INTO CountryList(sl_no, country, link, year, population, 
        yearly_percent_change, yearly_change, migrants_net, median_age, fertility_rate, density_p_km_percent, urban_pop_percent, 
        urban_population, countrys_share_of_world_pop, world_population, global_rank)
         VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        ( item['sl_no'], item['country'], item['link'], item['year'], item['population'], item['yearly_percent_change'],
          item['yearly_change'], item['migrants_net'], item['median_age'], item['fertility_rate'], item['density_p_km_percent'],item['urban_pop_percent'], 
          item['urban_population'], item['countrys_share_of_world_pop'], item['world_population'], item['global_rank'], ))
        self.conn.commit()
        return item


