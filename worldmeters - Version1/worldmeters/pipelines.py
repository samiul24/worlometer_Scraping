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
        print(1)
        self.create_table()
        print(2)

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS CountryList
        (Country Text)""")

    def process_item(self, item, spider):
        self.cur.execute("""INSERT OR IGNORE INTO CountryList VALUES(?)""",
        (item['name']))
        self.conn.commit()
        return item
