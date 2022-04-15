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
        (Name Text, Link Text, population Text, yearly_change Text, 
        net_change Text, lead_area Text, migrants Text, fert_rate Text, 
        med_age Text, urban_pop Text, world_share Text)""")

    def process_item(self, item, spider):
        self.cur.execute("""INSERT OR IGNORE INTO CountryList(name, link) VALUES(?, ?)""",
        ( item['name'], item['link'] ))
        self.conn.commit()
        return item
