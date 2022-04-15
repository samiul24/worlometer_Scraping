# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class WorldmetersPipeline:
    def __init__(self):
        self.conn = sqlite3.connect('ScrapyDB.db')
        self.cur = self.conn.cursor()
        self.create_table()


    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS CountryList
        (sl_no Text, country Text, link Text, year text, population Text, yearly_percent_change text, 
        yearly_change Text, migrants Text, median_age Text, fertility_rate Text, density Text, 
        urban_percent_pop Text, urban_population Text, country_share_of_world_pop Text, global_rank text)""")

    def process_item(self, item, spider):
        self.cur.execute("""INSERT OR IGNORE INTO CountryList VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        ( item['sl_no'], item['country'], item['link'], item['year'], item['population']
        , item['yearly_percent_change'], item['yearly_change'], item['migrants'], item['median_age']
        , item['fertility_rate'], item['density'], item['urban_percent_pop'], item['urban_population']
        , item['country_share_of_world_pop'], item['global_rank'] ))
        self.conn.commit()
        return item
