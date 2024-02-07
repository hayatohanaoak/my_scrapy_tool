# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
import datetime


class Nikkei500StockPipeline:
    def process_item(self, item, spider):
        return item

class NikkeiPipeline:
    def open_spider(self, spider):
        self.conn   = sqlite3.connect('NIKKEI.db')
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(
                '''
                CREATE TABLE tbl_stock_prices (
                    code int,
                    name str,
                    now real,
                    yen_comp real,
                    start real,
                    sup real,
                    inf real,
                    sell int,
                    per real,
                    dividend real,
                    insert_date str
                );
                '''
            )
            self.conn.commit()
        except:
            pass

    def process_item(self, item, spider):
        self.cursor.execute(
            '''
            INSERT INTO tbl_stock_prices (code, name, now, yen_comp, start, sup, inf, sell, per, dividend, insert_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            ''',
            (
                item.get('code'),
                item.get('name'),
                item.get('now'),
                item.get('yen_comp'),
                item.get('start'),
                item.get('sup'),
                item.get('inf'),
                item.get('sell'),
                item.get('per'),
                item.get('dividend'),
                str(datetime.date.today())
            )
        )
        self.conn.commit()
        return item
    
    def closeSpider(self, spider):
        self.conn.close()

